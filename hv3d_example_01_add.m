% Define the points and the reference point
points = [
    12, 9, 1;
    7, 15, 2;
    13, 3, 15;
    4, 5, 15;
    1, 17, 16
];
reference = [20, 20, 20];

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
    c1 = [0.4940 0.1840 0.5560]
    fill3([x0, x0+dx, x0+dx, x0], [y0, y0, y0, y0], [z0, z0, z0+dz, z0+dz], 'm');
    fill3([x0, x0+dx, x0+dx, x0], [y0+dy, y0+dy, y0+dy, y0+dy], [z0, z0, z0+dz, z0+dz], 'm');
    % Left and right faces
    c2 = [0.6350 0.2780 0.1840];
    fill3([x0, x0, x0, x0], [y0, y0+dy, y0+dy, y0], [z0, z0, z0+dz, z0+dz], 'm');
    fill3([x0+dx, x0+dx, x0+dx, x0+dx], [y0, y0+dy, y0+dy, y0], [z0, z0, z0+dz, z0+dz], 'm');
    % Top and bottom faces
    c3 = [0 0.5 0.5];
    fill3([x0, x0+dx, x0+dx, x0], [y0, y0, y0+dy, y0+dy], [z0+dz, z0+dz, z0+dz, z0+dz], 'm');
    fill3([x0, x0+dx, x0+dx, x0], [y0, y0, y0+dy, y0+dy], [z0, z0, z0, z0], 'm');
    alpha(0.5)
end

% Set the aspect ratio and limits for better visualization
axis equal;
xlim([0, 22]);
ylim([0, 22]);
zlim([0, 22]);
view(3);  % Set to 3D view

hold off;
