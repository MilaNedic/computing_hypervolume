% Define the points and the reference point
points = [
0.16 0.86 0.47; 
0.66 0.37 0.29; 
0.79 0.79 0.04; 
0.28 0.99 0.29; 
0.51 0.37 0.38;
0.92 0.62 0.07; 
0.16 0.53 0.70; 
0.01 0.98 0.94; 
0.67 0.17 0.54; 
0.79 0.72 0.05 
];
reference = [1, 1, 1];

% Sort points by z-coordinate
[~, idx] = sort(points(:,3));
points = points(idx,:);

% Prepare the figure
figure;
hold on;
grid on;
xlabel('X-axis');
ylabel('Y-axis');
zlabel('Z-axis');
title('3D Rectangular Volumes from Points to Reference Point');


    % Plot each point as a rectangular volume
for i = 1:size(points, 1)
    % Coordinates of the lower corner of the bar
    x0 = min(points(i, 1), reference(1));
    y0 = min(points(i, 2), reference(2));
    z0 = min(points(i, 3), reference(3));

    % Dimensions of the bar
    dx = abs(reference(1) - points(i, 1));
    dy = abs(reference(2) - points(i, 2));
    dz = abs(reference(3) - points(i, 3));

    % Draw the bar using vertices for each face
    % Front and back faces
    c1 = [0.5940 0.0840 0.5560]
    fill3([x0, x0+dx, x0+dx, x0], [y0, y0, y0, y0], [z0, z0, z0+dz, z0+dz], c1);
    fill3([x0, x0+dx, x0+dx, x0], [y0+dy, y0+dy, y0+dy, y0+dy], [z0, z0, z0+dz, z0+dz], c1);
    % Left and right faces

    fill3([x0, x0, x0, x0], [y0, y0+dy, y0+dy, y0], [z0, z0, z0+dz, z0+dz], c1);
    fill3([x0+dx, x0+dx, x0+dx, x0+dx], [y0, y0+dy, y0+dy, y0], [z0, z0, z0+dz, z0+dz], c1);
    % Top and bottom faces

    fill3([x0, x0+dx, x0+dx, x0], [y0, y0, y0+dy, y0+dy], [z0+dz, z0+dz, z0+dz, z0+dz], c1);
    fill3([x0, x0+dx, x0+dx, x0], [y0, y0, y0+dy, y0+dy], [z0, z0, z0, z0], c1);
    alpha(0.5)
end

axis equal;
xlim([0, 1.1]);
ylim([0, 1.1]);
zlim([0, 1.1]);
view(3);  % Set to 3D view

hold off;

