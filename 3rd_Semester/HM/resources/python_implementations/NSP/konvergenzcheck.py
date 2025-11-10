"""
Convergence checking and stopping criteria for iterative methods.
"""

import numpy as np
import matplotlib.pyplot as plt
from enum import Enum
from libraries import get_machine_epsilon

class ConvergenceCriterion(Enum):
    """Types of convergence criteria."""
    ABSOLUTE_STEP = 'absolute_step'
    RELATIVE_STEP = 'relative_step'
    ABSOLUTE_RESIDUAL = 'absolute_residual'
    RELATIVE_RESIDUAL = 'relative_residual'
    COMBINED = 'combined'

class ConvergenceChecker:
    """Class to check various convergence criteria."""
    
    def __init__(self, criterion, tol=1e-10, max_iter=100, rtol=1e-8):
        """
        Initialize convergence checker.
        
        Args:
            criterion: Type of convergence criterion to use
            tol: Absolute tolerance
            max_iter: Maximum number of iterations
            rtol: Relative tolerance
        """
        self.criterion = criterion
        self.tol = tol
        self.max_iter = max_iter
        self.rtol = rtol
    
    def check_convergence(self, x_new, x_old, f, iteration):
        """
        Check if convergence criteria are met.
        
        Args:
            x_new: Current approximation
            x_old: Previous approximation
            f: Function being solved
            iteration: Current iteration number
            
        Returns:
            Tuple of (convergence achieved, status message)
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
    
    def __init__(self, store_history=True):
        """
        Initialize convergence monitor.
        
        Args:
            store_history: Whether to store iteration history
        """
        self.iterations = []
        self.residuals = []
        self.step_sizes = []
        self.store_history = store_history
        
    def update(self, x_new, x_old, f):
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
            
    def estimate_convergence_rate(self):
        """
        Estimate convergence rate from stored history.
        
        Returns:
            Estimated convergence rate
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
        
    def get_convergence_history(self):
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
        
    def plot_convergence(self):
        """Plot convergence history."""
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

def run_iterative_method(f, x0, update_func, checker, monitor=None):
    """
    Run an iterative method with convergence checking.
    
    Args:
        f: Function to solve
        x0: Initial guess
        update_func: Function that returns next iteration
        checker: Convergence checker instance
        monitor: Optional convergence monitor
        
    Returns:
        Dict containing results and convergence info
    """
    x_old = x0
    converged = False
    iteration = 0
    
    while not converged and iteration < checker.max_iter:
        x_new = update_func(x_old)
        
        if monitor is not None:
            monitor.update(x_new, x_old, f)
        
        converged, msg = checker.check_convergence(x_new, x_old, f, iteration)
        
        if converged:
            return {
                'solution': x_new,
                'iterations': iteration + 1,
                'message': msg,
                'residual': abs(f(x_new)),
                'convergence_rate': monitor.estimate_convergence_rate() if monitor else None
            }
            
        x_old = x_new
        iteration += 1
        
    return {
        'solution': x_new,
        'iterations': iteration,
        'message': 'Maximum iterations reached',
        'residual': abs(f(x_new)),
        'convergence_rate': monitor.estimate_convergence_rate() if monitor else None
    }

# Example usage
if __name__ == "__main__":
    # Test function
    def f(x):
        return x**2 - 2
    
    # Newton's method update function
    def df(x):
        return 2*x
    def newton_update(x):
        return x - f(x)/df(x)
    
    # Create convergence checker with combined criteria
    checker = ConvergenceChecker(
        criterion=ConvergenceCriterion.COMBINED,
        tol=1e-10,
        rtol=1e-8,
        max_iter=100
    )
    
    # Create convergence monitor
    monitor = ConvergenceMonitor()
    
    # Run Newton's method
    result = run_iterative_method(f, 2.0, newton_update, checker, monitor)
    
    # Print results
    print(f"Results for √2 computation:")
    print(f"Solution: {result['solution']}")
    print(f"Iterations: {result['iterations']}")
    print(f"Message: {result['message']}")
    print(f"Final residual: {result['residual']}")
    print(f"Convergence rate: {result['convergence_rate']:.2f}")
    
    # Plot convergence history
    monitor.plot_convergence()
