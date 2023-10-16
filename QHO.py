import numpy as np
from numpy.fft import fft, ifft, rfft, irfft
import matplotlib.pyplot as plt

# Constants (Normally this are variable in exploratory version of code)
tol = 10**-9
N = 2**10
pi = np.pi
xlength = 6*pi
dx = xlength/N
# teporary x used to create various gaussians and potential functions.
x_temp = np.arange(-xlength/2, xlength/2-dx, dx)
c = 3
K = 2*pi/xlength * np.concatenate((np.arange(N/2), np.arange(-N/2, 0)))
LAP = -K**2
# External potential(In this case, a harmonic oscillator)
Vext = .5*x_temp**2
# Define acceleration matrix (Note, for my purposes, M = M^-1 because I
# never use it any other way
fftM = 1/(c-LAP)
# Build imaginary timestep using operators
L = (-LAP + Vext)
ML = fftM*L
LML = -LAP*ML + Vext*ML
MLML = fftM*LML
Dt = 3/max(MLML)
gaussian = np.exp(-10*x_temp**2)

def post_qho_first(n):
    run_data = {}
    # Initialize
    run_data['X'] = np.arange(-xlength/2, xlength/2-dx, dx).round(4).tolist()
    run_data['num_iters'] = 2
    run_data['error'] = -.5
    run_data['counter'] = 0
    run_data['mu_record'] = [n]
    run_data['error_record'] = [-.5]
    run_data['itarray'] = [0]
    run_data['done'] = False
    run_data['Vext'] = np.real(Vext).tolist()
    # Define initial conditions
    if n > 0:
        shift = int(N/(2**8)*(21.5*np.log(n+1) + 1))
        parity = -(2*(n%2) - 1)
        pos_gauss = gaussian
        neg_gauss = parity*gaussian
        run_data['u'] = (np.roll(neg_gauss, N - shift) + np.roll(pos_gauss, shift)).tolist()
    else:
        run_data['u'] = gaussian.tolist()
    return run_data

def post_qho_run(run_data):
    # Unpack run data
    X = np.array(run_data['X'])
    error = run_data['error']
    counter = run_data['counter']
    u = np.array(run_data['u'])
    # Run num_iters iterations
    run_data['num_iters'] = 1.5*run_data['num_iters']
    end = counter + run_data['num_iters']
    while (counter < end and not run_data['done']):
        u_old = u
        L00u = -.5 * ifft(LAP*fft(u)) + Vext*u
        M_u = ifft(fftM*fft(u))
        mu = (np.sum(M_u*L00u))/np.sum(u*M_u)
        L0u = L00u - mu*u
        M_L0u = ifft(fftM*fft(L0u))
        L1_M_L0u = -.5 * ifft(LAP*fft(M_L0u)) + Vext*M_L0u - mu*M_L0u
        M_L1_M_L0u = ifft(fftM*fft(L1_M_L0u))
        gamma = np.sum(M_L1_M_L0u*u)/np.sum(u*M_u)
        Lhatu = L1_M_L0u - gamma*u
        M_Lhatu = ifft(fftM*fft(Lhatu))
        u = u - Dt*M_Lhatu
        u = u/np.sqrt(np.sum(u**2)*dx)
        error = np.real(np.sqrt(np.sum((u-u_old)**2)))
        counter += 1
        if (counter % 1000 == 0):
            run_data['mu_record'].append(np.real(mu))
            run_data['error_record'].append(np.log10(np.real(error)))
            run_data['itarray'].append(counter)
        if error < tol:
            run_data['done'] = True
            run_data['mu_record'].append(np.real(mu))
            run_data['error_record'].append(np.log10(np.real(error)))
            run_data['itarray'].append(counter)
    # Save to run data
    run_data['u'] = np.real(u).tolist()
    run_data['X'] = np.real(X).tolist()
    run_data['error'] = float(np.real(error))
    run_data['counter'] = int(counter)
    return run_data