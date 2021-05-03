lc = 0.01;
a = 0.1;
b = 0.1;
c = 0.1;


Point(1) = {0, 0, 0, lc};
Point(2) = {a, 0, 0, lc};
Point(3) = {a, b, 0, lc};
Point(4) = {0, b, 0, lc};
Point(5) = {0, b, c, lc};
Point(6) = {a, b, c, lc};
Point(7) = {a, 0, c, lc};
Point(8) = {0, 0, c, lc};
Point(9) = {2*a, 0, 0, lc};
Point(10) = {2*a, b, 0, lc};
Point(11) = {2*a, 0, c, lc};
Point(12) = {2*a, b, c, lc};


Line(1) = {8, 5};
Line(2) = {5, 6};
Line(3) = {6, 7};
Line(4) = {8, 7};
Line(5) = {2, 3};
Line(6) = {3, 4};
Line(7) = {4, 1};
Line(8) = {1, 2};
Line(9) = {1, 8};
Line(10) = {2, 7};
Line(11) = {3, 6};
Line(12) = {4, 5};
Line(13) = {2, 9};
Line(14) = {9, 10};
Line(15) = {10, 3};
Line(16) = {7, 11};
Line(17) = {11, 12};
Line(18) = {12, 6};
Line(19) = {9, 11};
Line(20) = {10, 12};


Line Loop(21) = {8, 5, 6, 7};
Plane Surface(22) = {21};
Line Loop(23) = {8, 10, -4, -9};
Plane Surface(24) = {23};
Line Loop(25) = {12, -1, -9, -7};
Plane Surface(26) = {25};
Line Loop(27) = {6, 12, 2, -11};
Plane Surface(28) = {27};
Line Loop(29) = {15, 11, -18, -20};
Plane Surface(30) = {29};
Line Loop(31) = {14, 20, -17, -19};
Plane Surface(32) = {31};
Line Loop(33) = {13, 19, -16, -10};
Plane Surface(34) = {33};
Line Loop(35) = {3, -10, 5, 11};
Plane Surface(36) = {35};
Line Loop(37) = {16, 17, 18, 3};
Plane Surface(38) = {37};
Line Loop(39) = {2, 3, -4, 1};
Plane Surface(40) = {39};
Line Loop(41) = {13, 14, 15, -5};
Plane Surface(42) = {41};


Surface Loop(43) = {26, 28, 22, 24, 40, 36};
Volume(44) = {43};
Surface Loop(45) = {42, 34, 32, 30, 38, 36};
Volume(46) = {45};


Physical Surface("Z") = {40, 38};
Physical Surface("NZ") = {22, 42};
Physical Surface("NX") = {26};
Physical Surface("X") = {32};
Physical Surface("NY") = {24, 34};
Physical Surface("Y") = {28, 30};
Physical Surface("IN") = {36};


Physical Volume("One") = {44};
Physical Volume("Two") = {46};

Transfinite Line "*" = 3;
Transfinite Surface "*";
Recombine Surface "*";
Transfinite Volume "*";