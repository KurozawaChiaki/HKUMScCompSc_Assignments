#align(center, text(17pt)[
    *COMP7906 Introduction to Cyber Security* \
    Assignment 3
])
#align(center, text(15pt)[ZHANG Hongyi])

= Q1
== PKC Screenshot
#image("images/pkc_screenshot.png")
The screenshot of the PKC of #link("www.google.com") in Firefox is shown above.

== Issuer (CA)
The issuer of the PKC is *Google Trust Services* according to the detailed information.

== Signing algorithm and the key length
In Firefox, the signing algorithm is shown as *RSA*. And the key length of it is *4096 bits*.

= Q2
== Alice's private key
$ n_A &= 77 \
&= 7 times 11 $
$ p = 7, q = 11 $
Since $e_A = 23$, and $e_A times d_A eq.triple 1 mod phi(n)$, 
$d_A = frac(k phi(n) + 1, e_A) = frac(60k + 1, 23), k in NN$.

Thus, we can calculate the value of $d_A$:
$ d_A = 47 $
So, Alice's private key $(d_A, n_A) = (47, 77)$.

== The value of the plaintext $m$
According to RSA, $m = c^(d_B) mod 91 = 82$.

So the plaintext $m$ is *82*.