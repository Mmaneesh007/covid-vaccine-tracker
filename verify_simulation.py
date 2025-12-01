import sys
import os
import numpy as np
from scipy.integrate import odeint

# Add project root to path
sys.path.append(os.getcwd())

try:
    from src.simulation import SIR_model
    print("[OK] Successfully imported SIR_model from src.simulation")
except ImportError as e:
    print(f"[FAIL] Failed to import SIR_model: {e}")
    sys.exit(1)

def test_sir_model():
    print("\nTesting SIR Model Logic...")
    
    # Test parameters
    N = 1000
    I0, R0 = 1, 0
    S0 = N - I0 - R0
    beta, gamma = 0.2, 0.1
    t = np.linspace(0, 160, 160)
    y0 = S0, I0, R0
    
    # Run model
    ret = odeint(SIR_model, y0, t, args=(N, beta, gamma))
    S, I, R = ret.T
    
    # Check 1: Conservation of population (S + I + R should always equal N)
    total_pop = S + I + R
    if np.allclose(total_pop, N):
        print("[OK] Conservation of population verified (S+I+R = N)")
    else:
        print("[FAIL] Conservation of population FAILED")
        print(f"Max deviation: {np.max(np.abs(total_pop - N))}")
        
    # Check 2: Initial conditions
    if np.isclose(S[0], S0) and np.isclose(I[0], I0) and np.isclose(R[0], R0):
        print("[OK] Initial conditions verified")
    else:
        print("[FAIL] Initial conditions FAILED")
        
    # Check 3: Dynamics (S should decrease, R should increase)
    if S[-1] < S[0]:
        print("[OK] Susceptible population decreases over time")
    else:
        print("[FAIL] Susceptible population did not decrease")
        
    if R[-1] > R[0]:
        print("[OK] Recovered population increases over time")
    else:
        print("[FAIL] Recovered population did not increase")

    print("\nSIR Model Verification Complete!")

if __name__ == "__main__":
    test_sir_model()
