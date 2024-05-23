points3d = [12 9 1; 7 15 2; 13 3 15; 4 5 15; 1 17 16; 20 20 20]
reference = [20 20 20]
x = points3d(:,1);
y = points3d(:,2);
z = points3d(:,3);
[k,a] = convhull(points3d);
figure
plot3(x,y,z,'.','MarkerSize',20,'MarkerEdgeColor',[0.4940 0.1840 0.5560])
grid on
title('Example points for hv3dplus')

figure
trisurf(k,x,y,z,'FaceColor','m')
alpha(0.3)
grid on
title('Convex hull for example points for hv3dplus')
