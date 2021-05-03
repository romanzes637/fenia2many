lc = 0.01;
Point(1) = {0, 0, 0, lc};
Point(2) = {0.1, 0, 0, lc};
Point(3) = {0.1, 0.1, 0, lc};
Point(4) = {0, 0.1, 0, lc};
Point(5) = {0, 0.1, 0.1, lc};
Point(6) = {0.1, 0.1, 0.1, lc};
Point(7) = {0.1, 0, 0.1, lc};
Point(8) = {0, 0, 0.1, lc};
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
Line Loop(14) = {3, -4, 1, 2};
Plane Surface(14) = {14};
Line Loop(16) = {6, 7, 8, 5};
Plane Surface(16) = {16};
Line Loop(18) = {6, 12, 2, -11};
Plane Surface(18) = {18};
Line Loop(20) = {12, -1, -9, -7};
Plane Surface(20) = {20};
Line Loop(22) = {9, 4, -10, -8};
Plane Surface(22) = {22};
Line Loop(24) = {10, -3, -11, -5};
Plane Surface(24) = {24};
Surface Loop(26) = {16, 18, 20, 14, 24, 22};
Volume(26) = {26};
Physical Point("point1") = {1};
Physical Point("point2") = {2};
Physical Surface("top") = {14};
Physical Surface("bottom") = {16};
Physical Surface("left") = {20};
Physical Surface("down") = {22};
Physical Surface("right") = {24};
Physical Surface("up") = {18};
Physical Volume("internal") = {26};
Transfinite Line "*" = 3;
Transfinite Surface "*";
Recombine Surface "*";
Transfinite Volume "*";