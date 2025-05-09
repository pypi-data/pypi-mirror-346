from typing import Callable, List, Dict, Optional, Tuple, Any
from collections import defaultdict, deque
import numpy as np
import random
import time
from abc import ABC, abstractmethod
from ..common.solution import Solution
from ..common.neighborhood import NeighborhoodGenerator
    
class TabuSearch:
    def __init__(
        self,
        initial_solution: Solution,
        neighborhood_generator: NeighborhoodGenerator,
        tabu_tenure: int = 10,
        aspiration_criteria: Optional[List[Callable[[Solution], bool]]] = None,
        update_metrics: Optional[Callable[[Solution], Dict]] = None,
        intensification: bool = True,
        diversification: bool = True,
        max_iterations: int = 100,
        diversification_frequency: int = 20,
        intensification_threshold: int = 3,
        patience: int = 15,
        dynamic_tenure: bool = True,
        frequency_memory_size: int = 100,
        elite_pool_size: int = 5,
        logger: Optional[Callable[[str], None]] = None
    ):
        """
        Initialise la recherche Tabu.
        
        Args:
            initial_solution: Solution de départ
            neighborhood_generator: Générateur de voisinage
            tabu_tenure: Durée initiale de la liste Tabu
            aspiration_criteria: Critères pour outrepasser Tabu
            intensification: Active le mode intensification
            diversification: Active le mode diversification
            max_iterations: Nombre max d'itérations
            max_time: Temps max d'exécution en secondes
            diversification_frequency: Fréquence de diversification
            intensification_threshold: Seuil pour l'intensification
            patience: Nombre d'itérations sans amélioration avant arrêt
            dynamic_tenure: Ajuste dynamiquement la tenure Tabu
            frequency_memory_size: Taille de la mémoire des fréquences
            elite_pool_size: Taille du pool de solutions d'élite
            logger: Fonction de logging
        """
        self.current_solution = initial_solution.copy()
        self.best_solution = initial_solution.copy()
        self.neighborhood = neighborhood_generator
        self.tabu_list = deque(maxlen=tabu_tenure)
        self.tabu_tenure = tabu_tenure
        self.aspiration_criteria = aspiration_criteria or []
        self.intensification = intensification
        self.diversification = diversification
        self.max_iterations = max_iterations
        self.iterations = 0
        self.best_iteration = 0
        self._frequency = defaultdict(int)
        self._frequency_memory = deque(maxlen=frequency_memory_size)
        self._elite_pool = deque(maxlen=elite_pool_size)
        self._update_elite_pool(self.best_solution)
        self.diversification_frequency = diversification_frequency
        self.intensification_threshold = intensification_threshold
        self.patience = patience
        self.no_improvement_count = 0
        self.dynamic_tenure = dynamic_tenure
        self.logger = logger or (lambda msg: None)
        self.update_metrics = update_metrics
        if update_metrics:
            self.metrics = update_metrics(self.current_solution)
        else:
            self.history = {
            'best_fitness': [],
            'current_fitness': [],
            'diversification_events': [],
            'tenure_changes': []
        }

    def run(self) -> Solution:
        """Exécute la recherche Tabu améliorée."""
        self._log("Starting Tabu Search")
        
        while not self._should_stop():
            neighbors = self._generate_neighbors()
            best_candidate = self._select_best_candidate(neighbors)
            
            if best_candidate:
                self._update_current_solution(best_candidate)
                self._update_best_solution(best_candidate)
                self._update_tabu_list(best_candidate)
                self._update_frequency(best_candidate)
                self._update_elite_pool(best_candidate)
                self._adjust_parameters()
                if self.update_metrics:
                    self.metrics=self.update_metrics(best_candidate)
                else:
                    self._update_history()
                
            self.iterations += 1
            
            # Diversification réactive si stagnation
            if self.no_improvement_count > self.patience // 2:
                self._reactive_diversification()
        
        self._log("Tabu Search completed")
        return self.best_solution
    
    def _update_current_solution(self, candidate: Solution):
        self.current_solution = candidate.copy()
        
    def _update_best_solution(self, candidate: Solution):
        if candidate.evaluate() > self.best_solution.evaluate():
            self.best_solution = candidate.copy()
            self.best_iteration = self.iterations
            self.no_improvement_count = 0
        else:
            self.no_improvement_count += 1
            
    def _generate_neighbors(self) -> List[Solution]:
        """Génère les voisins avec stratégies avancées."""
        base_neighbors = self.neighborhood.generate(self.current_solution)
        
        if not base_neighbors:
            return []
            
        # Intensification basée sur la fréquence et le pool d'élite
        if self.intensification:
            neighbors = self._apply_intensification(base_neighbors)
        else:
            neighbors = base_neighbors
            
        # Ajout de voisins provenant des solutions d'élite
        if self._elite_pool and random.random() < 0.2:
            elite_neighbor = random.choice(list(self._elite_pool))
            neighbors.extend(self.neighborhood.generate(elite_neighbor))
            
        return neighbors

    def _apply_intensification(self, neighbors: List[Solution]) -> List[Solution]:
        """Applique les stratégies d'intensification."""
        # Filtre par fréquence
        filtered = [
            sol for sol in neighbors 
            if self._frequency[hash(frozenset((sol.representation)))] < self.intensification_threshold
        ]
        
        # Si le filtre élimine trop de voisins, on en garde une partie
        if len(filtered) < max(3, len(neighbors) // 2):
            # Prend les moins fréquents parmi les éliminés
            sorted_neighbors = sorted(
                neighbors, 
                key=lambda x: self._frequency[hash(x)]
            )
            filtered.extend(sorted_neighbors[:len(neighbors) - len(filtered)])
            
        return filtered

    def _should_stop(self) -> bool:
        """Détermine si la recherche doit s'arrêter."""
        # Critères d'arrêt standards
        if self.iterations >= self.max_iterations:
            self._log("Stopping - Max iterations reached")
            return True
                
        if self.iterations - self.best_iteration > self.patience:
            self._log("Stopping - Patience exceeded")
            return True
            
        # Diversification périodique
        if (self.diversification and 
            self.iterations > 0 and 
            self.iterations % self.diversification_frequency == 0):
            self._apply_diversification()
            
        return False

    def _apply_diversification(self):
        """Applique une diversification avancée."""
        self._log("Applying diversification")
        self.history['diversification_events'].append(self.iterations)
        
        # Stratégie 1: Retour à une solution d'élite modifiée
        if self._elite_pool:
            elite = random.choice(list(self._elite_pool))
            self.current_solution = self._perturb_solution(elite)
        # Stratégie 2: Solution aléatoire basée sur la fréquence
        else:
            self.current_solution = self._generate_low_frequency_solution()
            
        self.no_improvement_count = 0

    def _reactive_diversification(self):
        """Diversification réactive en cas de stagnation."""
        self._log("Applying reactive diversification")
        self.history['diversification_events'].append(self.iterations)
        
        # Augmente la tenure Tabu pour favoriser l'exploration
        if self.dynamic_tenure:
            self.tabu_tenure = min(50, int(self.tabu_tenure * 1.5))
            self.tabu_list = deque(self.tabu_list, maxlen=self.tabu_tenure)
            self.history['tenure_changes'].append((self.iterations, self.tabu_tenure))
            
        # Perturbe significativement la solution courante
        self.current_solution = self._perturb_solution(self.best_solution)
        self.no_improvement_count = 0

    def _perturb_solution(self, solution: Solution) -> Solution:
        """Crée une version perturbée d'une solution."""
        # Implémentation dépendante du problème - exemple générique:
        neighbors = self.neighborhood.generate(solution)
        if neighbors:
            return random.choice(neighbors)
        return solution.copy()

    def _generate_low_frequency_solution(self) -> Solution:
        """Génère une solution peu visitée."""
        # À adapter selon le problème - exemple générique:
        return self.neighborhood.generate(self.current_solution)[0]

    def _update_tabu_list(self, best_candidate: Solution):
        """Met à jour la liste tabou avec gestion avancée."""
        move_hash = self._get_move_hash(frozenset((best_candidate.representation)))
        
        # Évite les doublons dans la liste Tabu
        if move_hash in self.tabu_list:
            self.tabu_list.remove(move_hash)
            
        self.tabu_list.append(move_hash)
        
        # Ajustement dynamique de la tenure
        if self.dynamic_tenure:
            if self.no_improvement_count > self.patience // 2:
                self.tabu_tenure = min(50, self.tabu_tenure + 1)
            elif random.random() < 0.1:
                self.tabu_tenure = max(5, self.tabu_tenure - 1)
                
            self.tabu_list = deque(self.tabu_list, maxlen=self.tabu_tenure)

    def _get_move_hash(self, candidate: Solution) -> int:
        """Génère un hash pour le mouvement entre current et candidate."""
        # Pour les complexes protéiques, on peut hasher la différence entre les solutions
        diff_added = frozenset(candidate.representation - self.current_solution.representation)
        diff_removed = frozenset(self.current_solution.representation - candidate.representation)
        return hash((diff_added, diff_removed))
    

    def _select_best_candidate(self, neighbors: List[Solution]) -> Optional[Solution]:
        """Sélectionne le meilleur candidat avec critères avancés."""
        if not neighbors:
            return None
            
        evaluated = [(n, n.evaluate()) for n in neighbors]
        evaluated.sort(key=lambda x: x[1], reverse=True)
        
        current_value = self.current_solution.evaluate()
        best_value = self.best_solution.evaluate()
        
        for candidate, score in evaluated:
            move_hash = self._get_move_hash(candidate)
            is_tabu = move_hash in self.tabu_list
            is_aspired = any(crit(candidate) for crit in self.aspiration_criteria)
            is_elite_improvement = score > best_value
            is_local_improvement = score > current_value
            
            # Critères d'aspiration étendus
            if (not is_tabu) or is_aspired or is_elite_improvement:
                if is_local_improvement or is_elite_improvement:
                    return candidate
                    
        # Si tous tabous, retourne le meilleur qui améliore la solution courante
        for candidate, score in evaluated:
            if score > current_value:
                return candidate
                
        return None

    def _update_frequency(self, solution: Solution):
        """Met à jour les fréquences avec mémoire limitée."""
        h = hash(frozenset((solution.representation)))
        self._frequency[h] += 1
        self._frequency_memory.append(h)

    def _update_elite_pool(self, candidate: Solution):
        """Met à jour le pool de solutions d'élite."""
        candidate_value = candidate.evaluate()
        
        # Ajoute si meilleure que la pire de l'élite ou si pool non plein
        if len(self._elite_pool) < self._elite_pool.maxlen:
            self._elite_pool.append(candidate.copy())
        else:
            worst_in_pool = min(sol.evaluate() for sol in self._elite_pool)
            if candidate_value > worst_in_pool:
                # Remplace la pire solution
                for i, sol in enumerate(self._elite_pool):
                    if sol.evaluate() == worst_in_pool:
                        self._elite_pool[i] = candidate.copy()
                        break

    def _adjust_parameters(self):
        """Ajuste dynamiquement les paramètres."""
        # Ajuste la fréquence de diversification
        if self.no_improvement_count > self.patience // 2:
            self.diversification_frequency = max(
                5, 
                self.diversification_frequency - 2
            )
        elif random.random() < 0.05:
            self.diversification_frequency = min(
                50,
                self.diversification_frequency + 2
            )

    def _update_history(self):
        """Met à jour l'historique de la recherche."""
        self.history['best_fitness'].append(self.best_solution.evaluate())
        self.history['current_fitness'].append(self.current_solution.evaluate())

    def _log(self, message: str):
        """Journalise les informations de la recherche."""
        self.logger(
            f"Iter {self.iterations}: {message} - "
            f"Best: {self.best_solution.evaluate():.4f} - "
            f"Current: {self.current_solution.evaluate():.4f} - "
            f"No improvement: {self.no_improvement_count}"
        )