# Top 100 Restaurants

A curated application for discovering, managing, and reviewing the top 100 restaurants for every year since incpetion.  
Data source comes from here: https://www.theworlds50best.com/list/1-50. 
This repository contains the codebase and documentation for all core features.

## Features

### 1. Restaurant Listing
- Displays a paginated list of the top 100 restaurants.
- Search and filter by cuisine, location, or rating.
- Sort by name, rating, or popularity.

### 2. Restaurant Details
- View detailed information for each restaurant:
    - Name, address, contact info
    - Cuisine type
    - Opening hours
    - Menu highlights
    - Photos and map location

### 3. User Reviews & Ratings
- Authenticated users can submit reviews and ratings.
- Reviews include text, star rating, and optional photos.
- Aggregate ratings displayed for each restaurant.

### 4. Favorites & Collections
- Users can add restaurants to their favorites.
- Create and manage custom collections (e.g., "Date Night", "Family Friendly").

### 5. Admin Panel
- Admins can add, edit, or remove restaurants.
- Moderate user reviews and manage user accounts.

### 6. Authentication & Authorization
- Secure user registration and login.
- Role-based access for users and admins.

### 7. Responsive Design
- Fully responsive UI for desktop and mobile devices.

## Getting Started

1. **Clone the repository:**
     ```bash
     git clone https://github.com/yourusername/top-100-restaurants.git
     cd top-100-restaurants
     ```

2. **Install dependencies:**
     ```bash
     npm install
     ```

3. **Configure environment variables:**
     - Copy `.env.example` to `.env` and update with your settings.

4. **Run the development server:**
     ```bash
     npm start
     ```

## Project Structure

```
/src
    /components      # Reusable UI components
    /pages           # Main application pages
    /api             # API routes and handlers
    /utils           # Utility functions
    /styles          # CSS/SCSS files
```

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes.
4. Open a pull request.

## License

This project is licensed under the MIT License.

## Contact

For questions or feedback, please open an issue or contact the maintainer.
