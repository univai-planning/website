<!-- cell:0 type:markdown -->
This path takes you from the foundations of probability theory through to the core sampling algorithms that underpin computational statistics and machine learning. You will build intuition through simulation at every step — tossing coins, running elections, estimating integrals — so that the mathematical abstractions always have a concrete, runnable counterpart.

The journey has three parts: you begin by learning the language of randomness — probability, distributions, and random variables; then discover how sampling from distributions leads to powerful guarantees via the Law of Large Numbers, the Central Limit Theorem, and Monte Carlo integration; and finally master three algorithms for generating samples from any target distribution.

<!-- cell:1 type:markdown -->
### Learning outcomes

By the end of this path you will be able to:

- State and apply the rules of probability, Bayes' theorem, and the definitions of marginal and conditional distributions
- Distinguish between probability mass functions, probability density functions, and cumulative distribution functions, and move between them
- Explain the Law of Large Numbers and the Central Limit Theorem, and use them to characterize the sampling distribution of the mean
- Estimate integrals using Monte Carlo methods and quantify the estimation error via the CLT
- Implement the inverse transform method and the Box-Muller algorithm to generate samples from a target distribution
- Implement basic and envelope-based rejection sampling, and reason about acceptance rates
- Implement importance sampling, choose a reasonable proposal distribution, and explain how the choice affects variance

<!-- cell:2 type:markdown -->
### Prerequisites

Comfort with calculus (integration, change of variables) and basic Python (NumPy, Matplotlib). No prior probability or statistics background is assumed — the path builds it from scratch.

[Start this path](/learning/probability/?path=intro-to-sampling&step=1){.btn .btn-primary}

<!-- cell:3 type:markdown -->
## Part 1: The Language of Randomness

Probability, distributions, and random variables — the vocabulary you need before anything else.

::: {.lp-step-card}
**1.** [Probability](/learning/probability/?path=intro-to-sampling&step=1)

Three ways to think about probability: symmetry, models, and long-run frequency, illustrated with coin-flip simulations. Covers the rules of probability, random variables, marginals, conditionals, and Bayes' theorem with the Sally Clark case.
:::

::: {.lp-step-card}
**2.** [Distributions](/learning/distributions.html?path=intro-to-sampling&step=2)

Defines cumulative distribution functions, probability mass functions, and probability density functions with coin-toss examples. Covers the Uniform and Bernoulli distributions, and conditional and marginal distributions.
:::

::: {.lp-step-card}
**3.** [Distributions Example: Elections](/learning/distrib-example/?path=intro-to-sampling&step=3)

Simulates the 2012 US presidential election using Bernoulli coin flips for each state based on PredictWise probabilities. Introduces the Binomial distribution, the CLT's Gaussian approximation, and polling uncertainty via Gallup data.
:::

<!-- cell:4 type:markdown -->
## Part 2: From Samples to Guarantees

What happens when you draw samples from a distribution, and why averages converge — the Law of Large Numbers, the Central Limit Theorem, and Monte Carlo integration.

::: {.lp-step-card}
**4.** [Expectations and the Law of Large Numbers](/learning/expectations/?path=intro-to-sampling&step=4)

Defines expected values, the Law of the Unconscious Statistician (LOTUS), and variance for discrete and continuous distributions. Demonstrates the Law of Large Numbers and its connection to the frequentist interpretation of probability.
:::

::: {.lp-step-card}
**5.** [Sampling and the Central Limit Theorem](/learning/samplingclt/?path=intro-to-sampling&step=5)

Builds sampling distributions from repeated coin-flip experiments, showing how the sample mean and its variance behave as sample size grows. Derives the Central Limit Theorem and the sampling distribution of the variance.
:::

::: {.lp-step-card}
**6.** [Basic Monte Carlo](/learning/basicmontecarlo/?path=intro-to-sampling&step=6)

Introduces Monte Carlo methods by estimating the area of a unit circle with random points. Covers the hit-or-miss method and rejection sampling as building blocks for Monte Carlo integration.
:::

::: {.lp-step-card}
**7.** [Monte Carlo Integration](/learning/montecarlointegrals/?path=intro-to-sampling&step=7)

Formalizes Monte Carlo integration using uniform random samples and LOTUS, then extends to multidimensional integrals. Uses the Central Limit Theorem to estimate integration error and compares convergence rates with classical quadrature.
:::

<!-- cell:5 type:markdown -->
## Part 3: Sampling Algorithms

Three techniques for drawing samples from a target distribution: inverse transform, rejection sampling, and importance sampling.

::: {.lp-step-card}
**8.** [The Inverse Transform](/learning/inversetransform/?path=intro-to-sampling&step=8)

Introduces the inverse transform method for generating samples from arbitrary distributions using uniform random variables and the inverse CDF. Includes the Box-Muller transform for generating normal samples as a special case.
:::

::: {.lp-step-card}
**9.** [Rejection Sampling](/learning/rejectionsampling/?path=intro-to-sampling&step=9)

Presents von Neumann's rejection sampling algorithm for drawing samples from distributions with known functional form. Covers the basic method and an enhanced version that uses an envelope distribution for better acceptance rates.
:::

::: {.lp-step-card}
**10.** [Importance Sampling](/learning/importancesampling/?path=intro-to-sampling&step=10)

Introduces importance sampling as a method for computing expectations and integrals by reweighting samples from a proposal distribution. Shows how choosing a good proposal concentrates computation in regions that contribute most to the integral.
:::
