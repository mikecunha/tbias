import matplotlib.pyplot as plt
import seaborn as sns
from scipy.special import comb
from math import log, exp


def plot_test(frame, title):
    """Scatter plot of effect size vs. p-value by embedding."""

    sns.set_context("notebook", font_scale=1.45)
    sns.set_style('ticks')
    splot = sns.lmplot(x='p_val', y='effect_size', data=frame,
                       fit_reg=False,
                       size=6,
                       aspect=2,
                       legend=False,
                       hue="embedding",
                       scatter_kws={"marker": "D",
                                    "s": 100})

    # Formatting
    plt.title(title)
    plt.xlabel('P-value')
    plt.ylabel('Effect Size')

    for i, txt in enumerate(frame.embedding):
        splot.ax.annotate('  '+txt, (frame.p_val.iat[i],
                          frame.effect_size.iat[i]))


def n_choose_k(n, k, exact=True):
    # uses gamma function and log space to avoid overflow
    return comb(n, k, exact, repetition=False)


def calc_criteria(n, α, S, exact=True):
    """
    The main part of the CSM check for early stopping.
    This is what's being compared to epsilon at each
    iteration to check for stopping. Here converted to
    work in log-space to avoid underflow/overflow.
    """
    very_large_num = n_choose_k(n, S, exact)

    b = log(very_large_num) + S*log(α) + (n-S)*log(1-α)

    return (n+1) * exp(b)


def find_interval(α, n, ε, method='naive'):
    """
    Find "implied" stopping boundaries for a specific n.

    This implements l_n and u_n as described on the bottom
    of page 3 in the paper.

    Note* This is expensive to calculate at n > 2500
    because it's repeatedly calling n_choose_k with large
    numbers and dependent on exact answers.
    """

    if method == 'naive':
        max_k = 0
        min_k = n
        for k in range(1,n+1):
            crit = calc_criteria(n, α, k, exact=True)
            if crit > ε:
                max_k = max(max_k, k)
                min_k = min(min_k, k)

        lower = min_k - 1
        upper = max_k + 1
        return lower, upper

    # else use a solver, this is faster but has unreliable
    # accuracy, I tried a few other solvers over intervals
    # in scipy.optimize with poor results
    def calc_min_boundary(k):
        crit = calc_criteria(n, α, k)
        if crit > ε:
            return k
        else:
            return n + k

    res = minimize_scalar(calc_min_boundary, bounds=(1,n), method='Bounded')
    lower = res.x

    def calc_max_boundary(k):
        crit = calc_criteria(n, α, k)
        if crit > ε:
            return 1 / k
        else:
            return n + k

    res = minimize_scalar(calc_max_boundary, bounds=(1,n), method='Bounded')
    upper = res.x

    return lower, upper


def CSM(gen_obs, α=0.05, max_n=10000, ε=0.001, args=None):
    """
    Confidence Sequence Method
    As described in https://arxiv.org/abs/1611.01675

    Inputs
    ======
    gen_obs: a function that will return a binary value as
      part of a sequence. 0 meaning an observed test
      statistic did not meet or exceed the original test
      statistic and 1 meaning an obversed test statistic
      did.
    α: boundary of the significance level you are trying to
      determine which side the estimated p-value falls on.
    max_n: maximum number of observed test statistics to
      collect
    ε: limit on the re-sampling risk, values from the
      paper were in the interval [0.01,0.0001]
    """

    s = 0  # num of times observed >= test stat

    for n in range(1,max_n+1):

        if args is not None:
            if gen_obs(*args) == 1:
                s += 1
        else:
            if gen_obs() == 1:
                s += 1

        criteria = calc_criteria(n, α, s, exact=True)

        if criteria <= ε:

            if n < 2500:
                # Get the interval we have escaped
                I_n = find_interval(α=α, n=n, ε=ε)
            else:
                I_n = (None, None)

            print('out of boundary at n =', n)
            print('s =', s, '   I_n =', I_n)
            print('p-value =', s/n)
            print('criteria =', str(float(criteria)))

            if I_n[0] == None:
                # Leave it up to user to infer if H_null is rejected
                p_obs = s/n
                return p_obs, None

            if s <= I_n[0]:
                print('reject the null')
                return s/n, True
            elif s >= I_n[1]:
                print('fail to reject the null at α =', α, 'significance level.')
                return s/n, False
            else:
                print('Something went wrong.')

            break

        if n == max_n:
            # FIXME - return 95% Conf Interval of p-val
            # Gandy 2009 says that it's the min/max of all/recent
            # estimates of p_hat
            print('Iterations exhausted, p-val =', s/n)

    p_obs = s/n
    return p_obs, None
