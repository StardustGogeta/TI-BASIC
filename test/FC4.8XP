# The following is a factor calculator in TI-BASIC
Prompt A
1->D
While sqrt(A)>=D
If remainder(A,D)=0
Then
Disp D,A/D
End
D+1->D
End
Disp "LIST COMPLETE"
