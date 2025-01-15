"""
Convergence checking and stopping criteria for iterative methods.
"""

from typing import Callable, Tuple, Dict, List
import numpy as np
from enum import Enum
from dataclasses import dataclass
from libraries import get_machine_epsilon

class ConvergenceCriterion(Enum):
    """Types of convergence criteria."""
    ABSOLUTE_STEP = 'absolute_step'
    RELATIVE_STEP = 'relative_step'
    ABSOLUTE_RESIDUAL = 'absolute_residual'
    RELATIVE_RESIDUAL = 'relative_residual'
    COMBINED = 'combined'

@dataclass
class ConvergenceChecker:
    """Class to check various convergence criteria."""
    
    criterion: ConvergenceCriterion
    tol: float = 1e-10
    max_iter: int = 100
    rtol: float = 1e-8  # For relative criteria
    
    def check_convergence(self,
                         x_new: float,
                         x_old: float,
                         f: Callable[[float], float],
                         iteration: int) -> Tuple[bool, str]:
        """
        Check if convergence criteria are met.
        
        Args:
            x_new: Current approximation
            x_old: Previous approximation
            f: Function being solved
            iteration: Current iteration number
            
        Returns:
            Tuple containing:
            - Whether convergence is achieved
            - Message describing status
        """
        if iteration >= self.max_iter:
            return False, f"Maximum iterations ({self.max_iter}) reached"
            
        if self.criterion == ConvergenceCriterion.ABSOLUTE_STEP:
            if abs(x_new - x_old) < self.tol:
                return True, "Absolute step size criterion met"
                
        elif self.criterion == ConvergenceCriterion.RELATIVE_STEP:
            if abs(x_new - x_old) < self.rtol * abs(x_new):
                return True, "Relative step size criterion met"
                
        elif self.criterion == ConvergenceCriterion.ABSOLUTE_RESIDUAL:
            if abs(f(x_new)) < self.tol:
                return True, "Absolute residual criterion met"
                
        elif self.criterion == ConvergenceCriterion.RELATIVE_RESIDUAL:
            f_new = f(x_new)
            if abs(f_new) < self.rtol * abs(f(x_old)):
                return True, "Relative residual criterion met"
                
        elif self.criterion == ConvergenceCriterion.COMBINED:
            f_new = f(x_new)
            abs_step = abs(x_new - x_old)
            rel_step = abs_step / abs(x_new) if abs(x_new) > 0 else abs_step
            abs_res = abs(f_new)
            rel_res = abs_res / abs(f(x_old)) if abs(f(x_old)) > 0 else abs_res
            
            if ((abs_step < self.tol or rel_step < self.rtol) and
                (abs_res < self.tol or rel_res < self.rtol)):
                return True, "Combined criteria met"
        
        return False, "Convergence criteria not yet met"

class ConvergenceMonitor:
    """Monitor convergence behavior during iteration."""
    
    def __init__(self, store_history: bool = True):
        """
        Initialize convergence monitor.
        
        Args:
            store_history: Whether to store iteration history
        """
        self.iterations = []
        self.residuals = []
        self.step_sizes = []
        self.store_history = store_history
        
    def update(self, 
               x_new: float,
               x_old: float,
               f: Callable[[float], float]) -> None:
        """
        Update monitor with new iteration data.
        
        Args:
            x_new: Current approximation
            x_old: Previous approximation
            f: Function being solved
        """
        if self.store_history:
            self.iterations.append(x_new)
            self.residuals.append(abs(f(x_new)))
            self.step_sizes.append(abs(x_new - x_old))
            
    def estimate_convergence_rate(self) -> float:
        """
        Estimate convergence rate from stored history.
        
        Returns:
            float: Estimated convergence rate
        """
        if len(self.step_sizes) < 3:
            return 0.0
            
        rates = []
        for i in range(len(self.step_sizes)-2):
            if self.step_sizes[i] > 0 and self.step_sizes[i+1] > 0:
                rate = np.log(self.step_sizes[i+2]/self.step_sizes[i+1]) / \
                       np.log(self.step_sizes[i+1]/self.step_sizes[i])
                if not np.isnan(rate) and not np.isinf(rate):
                    rates.append(rate)
                    
        return np.mean(rates) if rates else 0.0
        
    def get_convergence_history(self) -> Dict[str, List[float]]:
        """
        Get convergence history data.
        
        Returns:
            Dict containing convergence history
        """
        return {
            'iterations': self.iterations,
            'residuals': self.residuals,
            'step_sizes': self.step_sizes
        }
        
    def plot_convergence(self) -> None:
        """Plot convergence history."""
        import matplotlib.pyplot as plt
        
        if not self.store_history:
            print("No history stored")
            return
            
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Plot residuals
        ax1.semilogy(self.residuals, 'b.-', label='Residual')
        ax1.grid(True)
        ax1.set_xlabel('Iteration')
        ax1.set_ylabel('Residual (log scale)')
        ax1.set_title('Residual Convergence')
        ax1.legend()
        
        # Plot step sizes
        ax2.semilogy(self.step_sizes, 'r.-', label='Step size')
        ax2.grid(True)
        ax2.set_xlabel('Iteration')
        ax2.set_ylabel('Step size (log scale)')
        ax2.set_title('Step Size Convergence')
        ax2.legend()
        
        plt.tight_layout()
        plt.show()

# Example usage
if __name__ == "__main__":
    # Test function
    def f(x: float) -> float:
        return x**2 - 2
    
    # Create convergence checker with combined criteria
    checker = ConvergenceChecker(
        criterion=ConvergenceCriterion.COMBINED,
        tol=1e-10,
        rtol=1e-8,
        max_iter=100
    )
    
    # Create convergence monitor
    monitor = ConvergenceMonitor()
    
    # Simple iteration example (Newton's method)
    def df(x: float) -> float:
        return 2*x
    
    x_old = 2.0  # Initial guess
    converged = False
    iteration = 0
    
    while not converged and iteration < checker.max_iter:
        # Newton step
        x_new = x_old - f(x_old)/df(x_old)
        
        # Update monitor
        monitor.update(x_new, x_old, f)
        
        # Check convergence
        converged, msg = checker.check_convergence(x_new, x_old, f, iteration)
        if converged:
            print(f"Converged after {iteration+1} iterations: {msg}")
            print(f"Solution: {x_new}")
            print(f"Residual: {abs(f(x_new))}")
            
        x_old = x_new
        iteration += 1
    
    # Analyze convergence
    conv_rate = monitor.estimate_convergence_rate()
    print(f"\nEstimated convergence rate: {conv_rate:.2f}")
    
    # Plot convergence history
    monitor.plot_convergence()
