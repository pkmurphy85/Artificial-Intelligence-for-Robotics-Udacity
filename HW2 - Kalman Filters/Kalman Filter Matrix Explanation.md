https://discussions.udacity.com/t/what-are-all-those-matrices-for-the-kalman-filter-part-i-x-f-p-h-r-u/57046

What are all those matrices for the Kalman filter? Part I: x, F, P, H, R, u
Courses Artificial Intelligence for Robotics
Mar 2012

Anne_PaulsonMar '12

Oh my gosh, you say, what the heck are all those Kalman matrices and vectors? I have no idea what’s going on, you say. Sebastian kind of threw them at us without a whole lot of explanation.

Ok, well, let’s try to figure them out a bit. Capital letters are for 2-D matrices, and bold lower case are for vectors, which are 1-D matrices.


Vector x, the variables


x is the values of all the variables you’re considering in your system. It might, for example, be position and velocity. Or if you were using a Kalman filter to model polling results, it might be Rick Santorum’s support and momentum in Ohio Presidential polls. It might be a sick person’s temperature and how fast the temperature is going up. It’s a vector. Let’s say it has n elements— that will be important for the size of other matrices.


For example, let’s say we’re modeling a sick person’s temperature. She’s lying there in the hospital bed with three temperature sensors stuck to her, and we want to see if her temperature is going up fast, in which case we’ll call a nurse. (For purposes of this example, we’ll assume that in the time period we’re observing, the rate of rise is constant.)


We might initialize x with a temperature of 98.6 and a temperature rising rate of 0. The Kalman filter algorithm will change x—that’s the whole point, to find the correct values for x.


Matrix F, the update matrix


F is the n by n update matrix. Kalman filters model a system over time. After each tick of time, we predict what the values of x are, and then we measure and do some computation. F is used in the update step. Here’s how it works:

For each value in x, we write an equation to update that value, a linear equation in all the variables in x. Then we can just read off the coefficients to make the matrix.


For our example, our x vector would be (x1, x2) where x1 is the temperature in degrees and x2 is the rate of change in hundredths of a degree (doesn’t matter whether Celsius or Fahrenheit, just as long as it’s the same for all) per minute. We check our sensors every minute, and update every minute.


Let’s figure out how to make the matrix F. If our patient's temperature is x1, what is it one minute later? It’s x1, the old temperature, plus the change. Note that because temperature is in degrees but the change is in hundredths of degrees, we have to put in the coefficient of 1/100.

<code>x[1]' = x[1] + x[2]/100
</code>
If the rate of change is x2, what is it one minute later? Still x2, because we’ve assumed the rate is constant.

<code>x[2]' = 0x[1] + x[2]
</code>
Now we write out all our equations, like this:

<code>x[1]' = x[1] + x[2]/100
x[2]' = 0x[1] + x[2]
</code>
In words, the new temperature, x1', is the old temperature plus the rise over the time segment. The new rate of change, x2', is the same as the old rate of change. We can just read off the coefficients of the right hand side, and there’s our matrix F:

<code>1 .01
0 1
</code>
Bingo. Note that these equations have to be linear equations in the variables. We might want to take the sine of a variable, or square it, or multiply two variables together. We can’t, though, not in a Kalman filter. These are linear equations.


z, the measurement vector


Now let’s turn to z, the measurement vector. It’s just the outputs from the sensors. Simple. Let’s say we have m sensors. That could be, and probably is, different from n, the number of variables we’re keeping track of. In our example, let’s say we have three temperature probes, all somewhat inaccurate.


H, the extraction matrix


The matrix H tells us what sensor readings we’d get if x were the true state of affairs and our sensors were perfect. It’s the matrix we use to extract the measurement from the data. If we multiply H times a perfectly correct x, we get a perfectly correct z.


So let’s figure out what z1, z2 and z3, the readings from our three temperature sensors, would be if we actually knew the patient’s temperature and rate of temperature rising, and our sensors were perfect. Again, we just write out our equations:

<code>z1 = x1 + 0x2
z2 = x1 + 0x2
z3 = x1 + 0x2
</code>
because if we knew the patients real temperature, and our sensors perfectly measured that temperature, z1 would be the same as x1 and so would z2 and z3.

Again, we just read off the coefficients to make H:

<code>1 0
1 0
1 0
</code>
Remember F, the update matrix, is n by n. Notice that H, the extraction matrix, is m by n. When we multiply H by x, we get a vector of size m.


P, the covariance matrix of x


P is the covariance matrix of the vector x. x is a vector of dimension n, so P is n by n. Down the diagonal of P, we find the variances of the elements of x: the bigger the number, the bigger our window of uncertainty for that element. On the off diagonals, at P[i][j], we find the covariances of x[i] with x[j]. Covariance matrices must be symmetric matrices, because the covariance of x[i] and x[j] is also the covariance of x[j] and x[i], so P[i][j]==P[j][i]. That is, the whole thing is symmetric down the main diagonal.


P gets updated as we run our Kalman filter and become more certain of the value of the x vector.

For the patient example, we start out pretty uncertain. We’ll give pretty big variances to both x1, the temperature, and x2, the rate of change in temperature. We don’t have any notion that temperature and rise in temperature are correlated, so we’ll make the covariance 0. So the matrix will look like

<code>3 0
0 .1
</code>
R, the covariance matrix of the measurement vector z

<code>    .2 0  0
    0 .2 0
    0 0 .2
</code>
But if we knew that the measurements from the three sensors tended to be off in the same direction—maybe all of them read low if a fan is blowing in the room, and high if music is playing—then we’d put positive covariances for them:

<code>.2 .05 .05
.05 .2 .05
.05 .05 .2
</code>
u, the move vector


The last input matrix is the vector u. This one is pretty simple; it’s the control input, the move vector. It’s the change to x that we cause, or that we know is happening. Since we add it to x, it has dimension n. When the filter updates, it adds u to the new x.


I can’t think of a good example using our patient and our thermometers, but suppose we were modeling the location and velocity of an object, and in addition to watching it move, we could also give it a shove. In the prediction stage, we’d update the object’s location based on our velocity, but then with u we’d add to its position and velocity because we moved it. u can change for each iteration of the Kalman filter. In our examples in class, it’s always all zeros; we’re not moving anything ourselves, just watching it move.


This is part I of an explanation of all the matrices in the Kalman filter. I'm writing it up for myself to see if I understand what's going on. This is very much a work in progress and needs proofreading. Part II28 (sketchy right now) covers S, K and y. Part III24 has some general comments about how the Kalman filter works, what kind of problems it works for, and what kind of problems it doesn't work for.


Added by @jasa:


The State Variable Model

IMHO Sebastian should have introduced the State Variable Model (SVM) which underlies the Kalman Filter. Here goes my contribution to this already nice wiki description of the KF as shown in our unit and homework.


One of the most important models for describing dynamic discrete or discretized systems is the SVM. The SVM consists in a couple of equations: the state equation


x(k) = F x(k-1) + B u(k-1)


where F is the state transition matrix, and the measurement or output equation


y(k) = H x(k)


The names of vectors and matrices follow those used by Sebastian, although they are not the standard in the SVM (which are A, B, C and D matrices). Sebastian has discarded u(k) (and implicitely considered B=Identity) since it puts it at zero. The vector x holds the state variables (2D positions and velocities in our unit).


The Kalman filter applies to the SVM with the addition of one vector to each of the equations, which represent the Gaussian uncertainty in the state equation, w(k), and in the measurement, v(k). Thus:


x(k) = F x(k-1) + u(k-1) + w(k-1)


y(k) = H x(k) + v(k)


Sebastian postulated no uncertainity at system level, so w(k) and its covarianve matrix don't appear in the Kalman filter equations taught in this unit, but v(k) appears, and its covariance matrix is our matrix R.


Kalman deduced, from the SVM, the "best" possible estimator (in the sense of the minimum variance estimator) of the output variable in each step, y(k), and the Kalman filter equations were born. You can find the deduction of the KF equations in many books and papers around the Web.


So, to conclude, our KF equations are based in the SVM which can describe almost all dynamic systems (discrete, in our case). Also, since we are iteratively updating the vectors and matrices inside the measurements loop, using the same data structures, the time iteration index, k, disappears from our implementation.
