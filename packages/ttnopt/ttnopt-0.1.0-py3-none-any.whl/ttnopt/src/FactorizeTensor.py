from typing import Dict, Union

import numpy as np
import tensornetwork as tn
import copy

from ttnopt.src.DataEngine import DataEngine
from ttnopt.src.TTN import TreeTensorNetwork


class FactorizeTensor(DataEngine):
    """A class for ground state search algorithm based on DMRG.
    Args:
        psi: The instance of TTN Class
        target (np.array, optional): The target tensor
        init_bond_dim (int, optional): The bond dimension which are used to initialize tensors
        max_bond_dim (int, optional): The maximum bond dimension during updating tensors
        truncation_err (float, optional): The maximum truncation error during updating tensors
    """

    def __init__(
        self,
        psi: TreeTensorNetwork,
        max_bond_dim: int = 16,
    ):
        """Initialize a FactorizeTensor object.

        Args:
            psi (TreeTensorNetwork): The quantum state.
            target (np.ndarray): Target tensor.
            init_bond_dim (int, optional): Initial bond dimension. Defaults to 4.
            max_bond_dim (int, optional): Maximum bond dimension. Defaults to 16.
        """
        self.entanglement: Dict[int, float] = {}
        self.fidelity: Dict[int, float] = {}
        self.error: Dict[int, float] = {}
        self.bond_dim: Dict[int, int] = {}
        super().__init__(psi, max_bond_dim)

    def run(
        self,
        target: Union[np.ndarray, None] = None,
        opt_fidelity=False,
        opt_structure=0,
        fidelity_convergence_threshold=1e-8,
        entanglement_convergence_threshold=1e-8,
        max_num_sweep=5,
        converged_count=2,
        max_truncation_error=0.0,
        temperature: float = 0.0,
        tau: int = 0,
    ):
        """Run FactorizingTensor algorithm.

        Args:
            target (np.ndarray): Target tensor.
            opt_fidelity (bool, optional): If optimize the fidelity or not. Defaults to False.
            opt_structure (bool, optional): If optimize the tree structure or not. Defaults to False.
            fidelity_convergence_threshold (float, optional): Fidelity threshold for convergence. Defaults to 1e-8.
            entanglement_convergence_threshold (float, optional): Entanglement entropy threshold for automatic optimization. Defaults to 1e-8.
            max_num_sweep (int, optional): Maximum number of sweeps. Defaults to 5.
            converged_count (int, optional): Converged count. Defaults to 2.
            max_truncation_error (float, optimal): .
        """

        _ee_at_edge: Dict[int, float] = {}
        ee_at_edge: Dict[int, float] = {}
        _fidelity_at_edge: Dict[int, float] = {}
        fidelity_at_edge: Dict[int, float] = {}
        _error_at_edge: Dict[int, float] = {}
        bond_dim: Dict[int, int] = {}

        edges, _edges = copy.deepcopy(self.psi.edges), copy.deepcopy(self.psi.edges)

        converged_num = 0

        for sweep_num in range(max_num_sweep):
            temp = temperature * (2 ** (-sweep_num / tau))
            if converged_num > converged_count:
                break

            ee_at_edge = copy.deepcopy(_ee_at_edge)
            fidelity_at_edge = copy.deepcopy(_fidelity_at_edge)
            edges = copy.deepcopy(_edges)

            self.distance = self.initial_distance()
            self.flag = self.initial_flag()

            print("Sweep count: " + str(sweep_num))
            while self.candidate_edge_ids() != []:
                (
                    edge_id,
                    selected_tensor_id,
                    connected_tensor_id,
                    not_selected_tensor_id,
                ) = self.local_two_tensor()

                self.set_flag(not_selected_tensor_id)

                if opt_fidelity:
                    self.set_ttn_properties_at_one_tensor(edge_id, selected_tensor_id)
                    new_tensor = self.update_tensor(
                        target, [selected_tensor_id, connected_tensor_id]
                    )
                else:
                    iso1 = tn.Node(self.psi.tensors[selected_tensor_id])
                    gauge = tn.Node(self.psi.gauge_tensor)
                    iso1[2] ^ gauge[0]
                    iso1 = tn.contractors.auto(
                        [iso1, gauge], output_edge_order=[iso1[0], iso1[1], gauge[1]]
                    )
                    self.psi.tensors[selected_tensor_id] = iso1.tensor
                    self.set_ttn_properties_at_one_tensor(edge_id, selected_tensor_id)

                    iso1 = tn.Node(self.psi.tensors[selected_tensor_id])
                    iso2 = tn.Node(self.psi.tensors[connected_tensor_id])
                    iso1[2] ^ iso2[2]
                    new_tensor = tn.contractors.auto(
                        [iso1, iso2],
                        output_edge_order=[iso1[0], iso1[1], iso2[0], iso2[1]],
                    )

                psi_edges = (
                    self.psi.edges[selected_tensor_id][:2]
                    + self.psi.edges[connected_tensor_id][:2]
                )
                u, s, v, probability, error, edge_order = self.decompose_two_tensors(
                    new_tensor,
                    self.max_bond_dim,
                    opt_structure=opt_structure,
                    temperature=temp,
                    operate_degeneracy=False,
                    max_truncation_error=max_truncation_error,
                )

                self.psi.tensors[selected_tensor_id] = u
                self.psi.tensors[connected_tensor_id] = v
                self.psi.gauge_tensor = s
                (
                    self.psi.edges[selected_tensor_id][0],
                    self.psi.edges[selected_tensor_id][1],
                ) = (
                    psi_edges[edge_order[0]],
                    psi_edges[edge_order[1]],
                )
                (
                    self.psi.edges[connected_tensor_id][0],
                    self.psi.edges[connected_tensor_id][1],
                ) = (
                    psi_edges[edge_order[2]],
                    psi_edges[edge_order[3]],
                )

                self.distance = self.initial_distance()
                if target is not None:
                    fidelity = self.get_fidelity(
                        target,
                    )
                    print("Fidelity:", fidelity)
                    _fidelity_at_edge[self.psi.canonical_center_edge_id] = fidelity
                ee = self.entanglement_entropy(probability)
                _ee_at_edge[self.psi.canonical_center_edge_id] = ee
                ee_dict = self.entanglement_entropy_at_physical_bond(
                    new_tensor, psi_edges
                )
                for key in ee_dict.keys():
                    _ee_at_edge[key] = ee_dict[key]
                _error_at_edge[self.psi.canonical_center_edge_id] = error

                bond_dim[self.psi.canonical_center_edge_id] = (
                    self.psi.gauge_tensor.shape[0]
                )

            _edges = copy.deepcopy(self.psi.edges)

            # 終了判定
            sweep_num += 1
            if sweep_num > 2:
                diff_ee = [
                    np.abs(ee_at_edge[key] - _ee_at_edge[key])
                    for key in ee_at_edge.keys()
                ]
                diff_fidelity = [
                    np.abs(fidelity_at_edge[key] - _fidelity_at_edge[key])
                    for key in fidelity_at_edge.keys()
                ]
                if all(
                    [
                        set(edge[:2]) == set(_edge[:2]) and edge[2] == _edge[2]
                        for edge, _edge in zip(edges, _edges)
                    ]
                ):
                    if all(
                        [ee < entanglement_convergence_threshold for ee in diff_ee]
                    ) and all(
                        [
                            diff_fidelity < fidelity_convergence_threshold
                            for diff_fidelity in diff_fidelity
                        ]
                    ):
                        converged_num += 1
        print("Converged")

        self.entanglement = _ee_at_edge
        self.fidelity = _fidelity_at_edge
        self.error = _error_at_edge
        self.bond_dim = bond_dim

        return 0
