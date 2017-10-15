Prompt X,Y
Disp "VELOCITY?"
Prompt A
If A>0
Then
Prompt V
Disp "ANGLE=",round(sin⁻¹(9.81*√(X²+Y²)/V²)/2,2
Else
Prompt θ
Disp "VELOCITY=",round(√(9.81*√(X²+Y²)/sin(2θ)),2
End
Disp "RANGE=",round(√(X²+Y²),2
