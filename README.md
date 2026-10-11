# MovieOwl - A Simple Movie Manager

## Description

MovieOwl is a desktop application built using Python, SQLite, and PyQt which provides a simplified, intuitive and simple movie management system.

Personal management of a movie collection gets harder the bigger it grows. This is true in our digital age where movies can be scattered on different platforms. It can be hard to know what you own in and keep track of movies and their watch status, their reviews, their ratings and your personal notes especially with online services or manual writing.

MovieOwl solves this problem by packaging a movie record, recommendation, note and review systems all in one desktop application.

## Objectives
- To develop a single centralized desktop application for managing personal movie collections.
- To provide users a way to record the movies in their collection.
- To provide users the tools for creating, editing, and searching for movies.
- To allow users the ability to organize their movies through collections and favorites.
- To create a system for managing movie ratings, movie reviews and movie notes.
- To implement a movie recommendation system through random or score based selection.
- To display a simple dashboard for global movie collection statistics.
- To apply clean modular architecture, object oriented programming, database application and clean code practice in the development of the project.

## Features

### Dashboard
Display current database records and simple statistics in a neat, readable format.
- Allows the user to see the total number of movies.
- Allows the user to see the  number of movie watched.
- Allows the user to see the number of unwatched movies.
- Display recommended movies.
- Display dashboard at the start of application.
  
### Movie Management
Display table of movies.
- Allows adding of movies.
- Allows editing of movie details.
- Allows viewing movie details.
- Allows deleting of movie records.
- Allows user keyword searching, filtering by genres, by watch status.

### Watch status
Allows tracking of movie watch status.
- Allows tagging movie as watched.
- Allows tagging movie as unwatched

### Review
Allows writing personal opinion on a movie entry
- Allows users to rate a movie.
- Allows writing a review.
- Allows writing a note.
- Save each movie review persistently per movie.

### Recommendation
Allows recommendation in two ways, a random movie or through a score.
- Allows selection of a random movie and displays it’s details.
- Allows ranked recommendations on dashboard page. 
- Selects unwatched and highly rated movies in database.

### User Collection
Allows user created collections/playlists of movies.
- Allows creation of custom named collection.
- Allows adding of movies to one or more collection.
- A default collection called favorites exits and movie added to favorites are automatically added on it.


## Technologies used
  #### Programming Language
  - Python 3.14
  
  #### GUI Framework / Library
  - PyQt6 6.11.0.
  - Qt Style Sheets (QSS) for application styling
  
  #### Database
  - SQLite3

  #### Libraries, Other Tools and Resources
  - Python Standard Library.
  - Git for version control.
  - GitHub for source-code management and repository hosting.
  - VSCode for development environment.
  - Manrope font for the application interface.
  - SVG icons for the graphical interface.



## Project Structure
    MovieOwl/
    ├── Assets/
    │   ├── fonts/
    │   └── icons/
    ├── Styles/
    ├── db/
    │   └── database.py
    ├── features/
    │   ├── collections/
    │   │   ├── repository.py
    │   │   ├── service.py
    │   │   └── view.py
    │   ├── dashboard/
    │   ├── favorites/
    │   ├── main_Window/
    │   ├── manage_movies/
    │   ├── movie_picker/
    │   ├── recommendations/
    │   └── review_notes/
    ├── .env.example
    ├── .gitignore
    ├── main.py
    ├── Movies.db
    └── README.md

Feature module pattern
Each folder in features/ is organized the same way:
repository.py: 
service.py: 
view.py:
model.py:

Feature folders
dashboard/:
manage_movies/: 
review_notes/:
recommendations/: 
movie_picker/: 
collections/:
favorites/:
main_Window/:
  
## Installation and Setup

### Requirements
- Python 3.14
- Git
- PyQt6 (installed in step 4)

### Installation

1. Clone the repository:

```powershell
   git clone https://github.com/BrotherJorg/MovieOwl.git
   cd MovieOwl
```

2. Create a virtual environment:

```powershell
   python -m venv .venv
```

3. Activate the virtual environment.

Windows PowerShell:

```powershell
   .\.venv\Scripts\Activate.ps1
```

 macOS / Linux:

```bash
   source .venv/bin/activate
```

4. Install the required dependency:

```powershell
   pip install PyQt6
```

5. Run the application:

```powershell
   python main.py
```

When setup is successful, the application window opens on the Dashboard.

 ## How to Use the Application

1. **Launch the application.** Run `python main.py`. The Dashboard opens first and shows the collection statistics.

2. **Navigate between screens.** Use the sidebar to open Dashboard, Manage Movies, Movie Picker, Recommendations, Collections, and Favorites.

3. **Add a movie.** Open Manage Movies, choose the add option, fill in the movie details, and save. The new movie appears in the table with the watch status Unwatched.

4. **View, edit, or delete a movie.** Select a movie in the table to see its details, then edit or delete it.

5. **Search and filter.** Type a keyword in the search box to find movies. Use the filters to narrow the table by genre or watch status.

6. **Change the watch status.** Set a movie to Unwatched, Watching, or Watched.

7. **Rate and review a movie.** Open a movie's review screen to give it a rating, write a review, and add a personal note. Each movie keeps its own review and notes.

8. **Mark a favorite.** Toggle a movie as a favorite. It is added to the default Favorites collection, and you can browse it on the Favorites screen.

9. **Create a collection.** Open Collections, create a collection with a custom name, and add movies to it. A movie can belong to more than one collection.

10. **Pick a movie to watch.** Open Movie Picker to get a random movie and its details. Open Recommendations to see a ranked list of unwatched, highly rated movies.

11. **Read the Dashboard.** Return to the Dashboard to see the total number of movies, how many are Watched, Watching, and Unwatched, the number of movies per genre, and the average rating.




## OOP Implementation

MovieOwl was developed using object-oriented programming principles. The system is divided into classes with specific responsibilities, allowing different parts of the application to be organized and maintained independently.

### Important Classes and Objects

| Class | Purpose |
|---|---|
| `Database` | Manages the SQLite database connection and database initialization. |
| `MovieRepository` | Handles database operations related to movie records. |
| `MovieService` | Contains the application logic for movie management. |
| `ManageMoviesView` | Provides the graphical interface for adding, viewing, editing, deleting, searching, and filtering movies. |
| `CollectionRepository` | Handles database operations involving collections and movie-collection relationships. |
| `CollectionService` | Provides collection-related application logic. |
| `CollectionsView` | Provides the graphical interface for managing collections. |
| `FavoritesService` | Handles the logic for adding and removing movies from the Favorites collection. |
| `FavoritesView` | Displays movies currently marked as favorites. |
| `DashboardView` | Displays statistics and summary information from the database. |
| `RecommendationService` | Handles the logic used to generate movie recommendations. |
| `RecommendationsView` | Displays recommended movies to the user. |
| `MoviePickerService` | Handles random movie selection. |
| `MoviePickerView` | Provides the interface for randomly selecting a movie. |
| `ReviewNotesService` | Handles the logic for movie reviews and notes. |
| `ReviewNotesView` | Provides the interface for writing and viewing reviews and notes. |
| `MainWindow` | Acts as the main application window and manages navigation between features. |

### Encapsulation

Encapsulation is applied by assigning specific responsibilities to individual classes and controlling how different parts of the application interact.

For example, database operations are handled by repository classes rather than being performed directly by the graphical interface. Services also provide a layer between the views and repositories, allowing application logic to remain separate from the GUI.

### Inheritance

Inheritance is primarily used in the PyQt6 interface classes. Feature views inherit from Qt widget classes such as `QWidget` and `QMainWindow`.






### Database Structure
MovieOwl stores its data in a local SQLite database, `Movies.db`. The `Database` class in `db/database.py` opens the connection and creates the tables on startup if they don't exist, so the database is rebuilt automatically when the file is missing. The database has three tables: movies, collections, and a link table that connects them.

### Important Tables

**movies**: stores each movie record.

| Column | Type | Description |
|---|---|---|
| id | INTEGER, primary key, autoincrement | Unique movie ID |
| title | TEXT, required | Movie title |
| genre | TEXT, required | Movie genre |
| year | INTEGER, required | Release year |
| rating | REAL, required | User rating (TODO: scale, e.g. 0 to 10) |
| status | TEXT, required, default `Unwatched` | Watch status |
| review | TEXT, optional | Personal review |
| notes | TEXT, optional | Personal notes |

**collections**: stores user-created collections.

| Column | Type | Description |
|---|---|---|
| id | INTEGER, primary key, autoincrement | Unique collection ID |
| name | TEXT, required, unique | Collection name |

A default collection named Favorites is inserted automatically.

**movie_collections**: links movies to collections (many-to-many).

| Column | Type | Description |
|---|---|---|
| movie_id | INTEGER, foreign key | References movies(id) |
| collection_id | INTEGER, foreign key | References collections(id) |

The primary key is the pair (movie_id, collection_id), so a movie can be in many collections but only once in each. Both keys are defined with `ON DELETE CASCADE`.

### Database Operations

| Operation | What the system does | Example SQL |
|---|---|---|
| Create | Adds a movie, creates a collection, adds a movie to a collection or to Favorites | `INSERT INTO movies (title, genre, year, rating) VALUES (?, ?, ?, ?)` |
| Read | Loads the movie table and details, the collections, favorites, and the dashboard statistics | `SELECT * FROM movies` |
| Update | Edits a movie, changes its watch status, saves its review and notes | `UPDATE movies SET status = ? WHERE id = ?` |
| Delete | Removes a movie, or removes a movie from a collection | `DELETE FROM movies WHERE id = ?` |
| Search | Finds movies by keyword and filters by genre or watch status | `SELECT * FROM movies WHERE title LIKE ?` |

The Dashboard uses aggregate queries (`COUNT`, `AVG`, `GROUP BY genre`) for the totals, status counts, movies per genre, and the average rating.

## Screenshots
### Dashboard
<img width="2836" height="1765" alt="Dashboard" src="https://github.com/user-attachments/assets/3a3c0808-ca0f-4368-b707-20a83d960c0a" />

The initial page at startup that displays simplified information, such as total movies, movies per genre, movies watched or watching.

### Manage Movies
<img width="2858" height="1780" alt="Manage Movies" src="https://github.com/user-attachments/assets/d08f350d-e9c3-42dc-9630-af8c1d9dc35e" />
The main page where user add, edits and interacts with their collection, searching and filtering options are provide for moderate to large sized collections. It allows sorting in three layers. First is keyword search, Genre and then status which can be combined. Review, status update and favorites button are also in this page.

### Collections
<img width="2812" height="1747" alt="Collections" src="https://github.com/user-attachments/assets/fb9c6d0a-ed6f-4432-8c48-b98ea0495123" />
The page for user created collections, default collection is "favorites" movies toggled favorites are automatically added here. User can also create their own.

## Testing

The system was tested by performing the main operations and comparing the expected and actual results.

| Feature | Expected Result | Actual Result |
|---|---|---|
| Add/Edit/Delete Movie | Movie data is correctly changed | Passed |
| Search & Filter | Matching movies are displayed | Passed |
| Watch Status | Selected status is saved | Passed |
| Reviews & Notes | Information is saved and displayed | Passed |
| Collections | Movies can be added and removed | Passed |
| Favorites | Movies can be added or removed from Favorites | Passed |
| Dashboard | Statistics reflect current data | Passed |
| Recommendations | Recommendations are generated | Passed |
| Movie Picker | A movie is randomly selected | Passed |

## Known Issues / Limitations

- Movie information must be entered manually.
- The application does not currently use an external movie API.
- The system is designed for local, single-user use.


## Author
Garth June Saballa
CS26, 3581, 2026-2027


