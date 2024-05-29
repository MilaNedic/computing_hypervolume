% Define the points and the reference point
points = [
3 4 18; 
1 10 16; 
5 2 20; 
8 1 19;
4 5 19
];
reference = [21, 21, 21];

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
    c1 = [0.1 0.1 0.8];
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
xlim([0, 22]);
ylim([0, 22]);
zlim([0, 22]);
view(3);  % Set to 3D view

hold off;
