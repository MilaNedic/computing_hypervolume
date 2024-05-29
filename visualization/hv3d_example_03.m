% Define the points and the reference point
points = [
6.065302  9.935803  0.057723;
5.458772  8.942222  0.051951;
9.021428  8.957610  9.484568;
7.217142  7.166088  7.587655;
9.977956  5.982049  5.050338;
6.984569  4.187434  3.535236;
2.482368  4.216830  2.333960;
6.699873  4.403164  5.164936;
2.941581  1.768941  8.103145;
7.449828  0.908397  7.228283
];
reference = [10, 10, 10];

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
title('3D Rectangular Volumes from Points to Reference');

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
    c1 = [0.3 0.3 0.4];
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

% Set the aspect ratio and limits for better visualization
axis equal;
xlim([0, 11]);
ylim([0, 11]);
zlim([0, 11]);
view(3);  % Set to 3D view

hold off;
