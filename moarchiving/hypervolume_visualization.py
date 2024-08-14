import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from moarchiving import MOArchive
from moarchiving2d import BiobjectiveNondominatedSortedList
from test_moarchiving import get_non_dominated_points_3d


def main():
    fig = go.Figure(data=[
        go.Mesh3d(
            # 8 vertices of a cube
            x=[0, 0, 1, 1, 0, 0, 1, 1],
            y=[0, 1, 1, 0, 0, 1, 1, 0],
            z=[0, 0, 0, 0, 1, 1, 1, 1],
            # Intensity of each vertex, which will be interpolated and color-coded
            # i, j and k give the vertices of triangles
            i = [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
            j = [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
            k = [0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
            name='y',
            showscale=True
        )
    ])

    # add a scatter plot to the figure
    fig.add_trace(go.Scatter3d(
        x=[0, 1],
        y=[0, 1],
        z=[0, 1],
        mode='markers',
        marker=dict(
            size=12,
            color='rgb(0, 0, 0)',                # set color to black
            symbol='circle',                    # set symbol to circle
            line=dict(
                color='rgb(0, 0, 0)',            # set line color to black
                width=0.5
            )
        )
    ))

    fig.show()


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


def draw_hypervolume(points, ref_point):
    points = points.tolist()
    moa = MOArchive(points, ref_point)
    points = moa.points_list

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
            color='rgb(160, 160, 160)',                # set color to black
            symbol='circle',                    # set symbol to circle
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
                color='rgb(0, 0, 0)',                # set color to black
                symbol='x',                    # set symbol to circle
                line=dict(
                    color='rgb(0, 0, 0)',            # set line color to black
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

    """
    # remove the axis numbers
    fig.update_layout(scene=dict(
        xaxis=dict(
            showticklabels=False,
            showgrid=False,
            title=''
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False,
            title=''
        ),
        zaxis=dict(
            showticklabels=False,
            # also hide grid lines
            showgrid=False,
            # also hide axis name
            title=''
        ),
        bgcolor='white',
        xaxis_visible=False, yaxis_visible=False, zaxis_visible=False
    ))
    """
    fig.show()


def random_3d_structure(n_points):
    points = np.random.rand(n_points, 3)
    ref_point = [1, 1, 1]
    draw_hypervolume(points, ref_point)


def plot_non_dominated__points(n_points=1000, mode="spherical"):
    points = get_non_dominated_points_3d(n_points, mode=mode)

    fig = go.Figure(data=[
        go.Scatter3d(
            x=points[:, 0],
            y=points[:, 1],
            z=points[:, 2],
            mode='markers',
            marker=dict(
                size=4,
                color='rgb(0, 0, 0)',                # set color to black
                symbol='x',                    # set symbol to circle
                line=dict(
                    color='rgb(0, 0, 0)',            # set line color to black
                    width=0.5
                )
            )
        )
    ])
    fig.show()


if __name__ == '__main__':
    pts = np.array(
        [[1, 2, 3], [2, 3, 1], [3, 1, 2]]
    )
    # draw_hypervolume(pts, [4, 4, 4])
    plot_non_dominated__points(1000, mode="linear")
    plot_non_dominated__points(1000, mode="spherical")
