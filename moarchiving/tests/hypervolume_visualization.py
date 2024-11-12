import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from moarchiving.moarchiving3d import MOArchive3d
from moarchiving.tests.test_moarchiving3d import get_non_dominated_points


def draw_point(point, ref_point, fig):
    # draw a cube with the point as one of the vertices and the ref_point as the opposite vertex
    fig.add_trace(go.Mesh3d(
        # 8 vertices of a cube
        x=[point[0], point[0], ref_point[0], ref_point[0], point[0], point[0], ref_point[0], ref_point[0]],
        y=[point[1], ref_point[1], ref_point[1], point[1], point[1], ref_point[1], ref_point[1], point[1]],
        z=[point[2], point[2], point[2], point[2], ref_point[2], ref_point[2], ref_point[2], ref_point[2]],
        # Intensity of each vertex, which will be interpolated and color-coded
        # i, j and k give the vertices of triangles
        i=[7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
        j=[3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
        k=[0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
        name='y',
        showscale=True
    ), row=1, col=1)


def draw_hypervolume_with_kink_points(points, ref_point):
    moa = MOArchive3d(points, ref_point)
    points = moa.points

    fig = make_subplots(rows=1, cols=1,
                        specs=[[{'type': 'surface'}]])

    # add a scatter plot to the figure
    fig.add_trace(go.Scatter3d(
        x=[ref_point[0]],
        y=[ref_point[1]],
        z=[ref_point[2]],
        mode='markers',
        marker=dict(
            size=8,
            color='rgb(160, 160, 160)',
            symbol='circle',
        ),
        name="ref_point"
    ), row=1, col=1)

    for p in points:
        draw_point(p, ref_point, fig)
        fig.add_trace(go.Scatter3d(
            x=[p[0]],
            y=[p[1]],
            z=[p[2]],
            mode='markers',
            marker=dict(
                size=4,
                color='rgb(0, 0, 0)',
                symbol='x',
                line=dict(
                    color='rgb(0, 0, 0)',
                    width=0.5
                )
            ),
            name=str(p)
        ), row=1, col=1)
    eps = ref_point[0] / 100

    kink_points = moa._get_kink_points()

    for k in kink_points:
        fig.add_trace(go.Scatter3d(
            x=[k[0] - eps],
            y=[k[1] - eps],
            z=[k[2] - eps],
            mode='markers',
            marker=dict(
                size=10,
                color='rgb(0, 0, 0)',
                symbol='circle',
            ),
            name=str(k)
        ), row=1, col=1)

    # set axis limits between 0 and ref_point
    fig.update_layout(scene=dict(
        xaxis=dict(range=[0, ref_point[0]]),
        yaxis=dict(range=[0, ref_point[1]]),
        zaxis=dict(range=[0, ref_point[2]]),
        aspectmode='cube'
    ))

    fig.show()


def main():
    n_points = 20
    ref_point = [1, 1, 1]

    # plot 20 random points in 3d space
    # points = np.random.rand(20, 3)
    # draw_hypervolume_with_kink_points(points, ref_point)

    # plot 20 non-dominated points in 3d space
    # non_dominated_points = get_non_dominated_points(20, 3)
    # draw_hypervolume_with_kink_points(non_dominated_points, ref_point)

    # custom points
    draw_hypervolume_with_kink_points([[1, 2, 3], [2, 3, 2], [3, 2, 1]], [4, 4, 4])


if __name__ == "__main__":
    main()
