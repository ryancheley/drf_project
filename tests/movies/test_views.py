import pytest

from movies.models import Movie


@pytest.mark.django_db
def test_add_movie(client):
    movies = Movie.objects.all()
    assert len(movies) == 0

    resp = client.post(
        "/api/movies/",
        {"title": "The Big Lebowski", "genre": "comedy", "year": "1998", },
        content_type="application/json",
    )
    assert resp.status_code == 201
    assert resp.data["title"] == "The Big Lebowski"

    movies = Movie.objects.all()
    assert len(movies) == 1


@pytest.mark.django_db
def test_remove_movie(client, add_movie):
    movie = add_movie(title="The Big Lebowski", genre="comedy", year="1998")

    resp = client.get(f"/api/movies/{movie.id}/")
    assert resp.status_code == 200
    assert resp.data["title"] == "The Big Lebowski"

    resp_two = client.delete(f"/api/movies/{movie.id}/")
    assert resp_two.status_code == 204

    resp_three = client.get("/api/movies/")
    assert resp_three.status_code == 200
    assert len(resp_three.data) == 0


@pytest.mark.django_db
def test_remove_movie_incorrect_id(client):
    resp = client.delete(f"/api/movies/99/")
    assert resp.status_code == 404


@pytest.mark.django_db
def test_update_movie(client, add_movie):
    movie = add_movie(title="The Big Lebowski", genre="comedy", year="1998")

    resp = client.put(
        f"/api/movies/{movie.id}/",
        {"title": "The Big Lebowski", "genre": "comedy", "year": "1997"},
        content_type="application/json",
    )
    assert resp.status_code == 200
    assert resp.data["title"] == "The Big Lebowski"
    assert resp.data["year"] == "1997"

    resp_two = client.get(f"/api/movies/{movie.id}/")
    assert resp_two.status_code == 200
    assert resp_two.data["title"] == "The Big Lebowski"
    assert resp.data["year"] == "1997"


@pytest.mark.django_db
def test_update_movie_incorrect_id(client):
    resp = client.put(f"/api/movies/99/")
    assert resp.status_code == 404


@pytest.mark.django_db
@pytest.mark.parametrize(
    "add_movie, payload, status_code",
    [
        ["add_movie", {}, 400],
        ["add_movie", {"title": "The Big Lebowski", "genre": "comedy"}, 400],
    ],
    indirect=["add_movie"],
)
def test_update_movie_invalid_json(client, add_movie, payload, status_code):
    movie = add_movie(title="The Big Lebowski", genre="comedy", year="1998")
    resp = client.put(
        f"/api/movies/{movie.id}/", payload, content_type="application/json",
    )
    assert resp.status_code == status_code
