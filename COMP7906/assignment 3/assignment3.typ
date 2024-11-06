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
The issuer of the PKC is *Google Trust Services LLC* according to the detailed information.

== Signing algorithm and the key length
In Firefox, the signing algorithm is shown as *RSA*. And the key length of it is *4096 bits*.

= Q2
== Alice's private key
$ n_A &= 77 \
&= 7 times 11 $
So we can choose $p = 7, q = 11$.

Since $e_A = 23$, and $e_A times d_A eq.triple 1 mod phi(n)$, 
$d_A = frac(k phi(n) + 1, e_A) = frac(60k + 1, 23), k in NN$,
we can calculate the value of $d_A$:
$ d_A = 47 $
So, Alice's private key $(d_A, n_A) = (47, 77)$.

== The value of the plaintext $m$
According to RSA, $m = c^(d_B) mod 91 = 82$.

So the plaintext $m$ is *82*.

= Q3
== How can B show evidence to prove A had sent message?
B can use his own private key $B_("pri")$ to decrypt the transmitted message, 
which includes A's signature and PKC.

Then B can obtain the public key $A_("pub")$ corresponding to A's private key $A_("prv")$ by the PKC to verify the aforementioned signature
to ensure it belongs to A, which can prove the message was sent by A.

== How can B be sure that another person D cannot get the plaintext?
The message was sent between A and B using asymmetric encryption method. According to the schema, the message was encrypted using the public key $B_("pub")$.
Hence, it is computationally infeasible for D to derive $B_("priv")$ from $B_("pub")$ or to break the encryption to get the plaintext, 
as long as the private key $B_("pri")$ is well kept as secret.

== Which properties of the cryptographic hash function prevent an attacker from froging the signature?
- #strong[One-way Property]: Given any value $y$, it is infeasible to find a value $x$ such that $h(x) = y$.
  This property makes sure that attackers cannot come up with a fake message and keep the same signature as the original one.
- *Second-preimage Resistance*: Given $h(x)$ and $x$, it is infeasible to find $y eq.not x$ such that $h(x) = h(y)$.
  This property ensures that attackers cannot find another message producing the same hash result as the original message.

Apart from these properties mentioned in the slides, the cryptographic hash function can compute the hash value quickly and the result of the same plaintext is always the same. 
The length of the output of the hash function is fixed as well.

= Q4