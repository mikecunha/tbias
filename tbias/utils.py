import matplotlib.pyplot as plt
import seaborn as sns
from scipy.special import comb


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


def n_choose_k(n, k):
    # uses gamma function and log space to avoid overflow
    return comb(n, k, exact=False, repetition=False)


def calc_criteria(n,α,S):
    """
    The main part of the CSM check for early stopping.
    """

    very_large_num = n_choose_k(n,S)
    very_small_num = (α**S)*((1-α)**(n-S))

    # avoid underflow
    if very_small_num == 0:
        b = 0
    else:
        b = very_large_num * very_small_num

    return (n+1) * b


def CSM(gen_obs, α=0.05, max_n=10000, ε=0.001):
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

        if gen_obs() == 1:
            s += 1

        # Enforce a bare minimum of iters
        if n < 499:
            continue

        criteria = calc_criteria(n, α, s)

        if criteria <= ε:
            print('out of boundary at n =', n)
            print('criteria: ', str(float(criteria)))
            print('p-value =', s/n)
            if 0 >= criteria and criteria <= α:
                print('reject the null')
            elif α > criteria and criteria <= 1:
                print('fail to reject the null')
            else:
                print('hmmm something not right: ', float(criteria))
            break

        if n == 10000:
            print('Iterations exhausted, p-val =', s/n)

    return n, s
