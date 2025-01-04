# Social Media API

## Project Overview
This Social Media API is designed to provide backend functionality for a social media platform. It enables users to create and manage posts, establish relationships through a follow system, and view a personalized feed. Built using Django and Django REST Framework (DRF), the project emphasizes CRUD operations, user authentication, and efficient database interactions to simulate a real-world social media environment.

---

## Core Functionalities

### 1. Post Management (CRUD)
- **Features**:
  - Users can Create, Read, Update, and Delete their posts.
  - Each post includes the following attributes:
    - **Content** (text): Required.
    - **User** (author): Required.
    - **Timestamp**: Auto-generated.
    - **Media** (optional): URLs for image uploads.
- **Validations**:
  - Content and User fields are required.
  - Users can only update or delete their own posts.

### 2. User Management (CRUD)
- **Features**:
  - Users can register, update, and delete their accounts.
  - Each user has:
    - **Username**: Unique and required.
    - **Email**: Unique and required.
    - **Password**: Securely stored.
    - **Profile**:
      - Optional fields: Bio and Profile Picture.
- **Authentication**:
  - Only authenticated users can manage their profiles and posts.

### 3. Follow System
- **Features**:
  - Users can follow and unfollow other users.
  - A system tracks the follower and following relationships.
- **Validations**:
  - Users cannot follow themselves.
  - Relationships are stored efficiently in the database.

### 4. Feed of Posts
- **Features**:
  - Users can view a feed displaying posts from the users they follow.
  - Posts are displayed in reverse chronological order (most recent first).
  - Filters allow searching posts by keywords or date.
- **Pagination**:
  - Feeds are paginated for users with a large volume of posts.
  - Sorting options include sorting by Date or Popularity (likes, comments).

---

## Technical Implementation

### Database
- **Models**:
  - **User**: Handles user authentication and profile information.
  - **Post**: Stores post data and links posts to users.
  - **Follow**: Tracks follower-following relationships.
- **Django ORM**: Used to efficiently interact with the database.

### Authentication
- **Features**:
  - Token-based authentication using JWT.
  - Users must log in to create, update, or delete posts, follow/unfollow users, or view their feed.

### API Design
- **Django REST Framework**:
  - RESTful endpoints using appropriate HTTP methods (GET, POST, PUT, DELETE).
  - Comprehensive error handling with relevant HTTP status codes (e.g., 404 for Not Found, 400 for Bad Request).

---

## Deployment
- The API is deployed on **Render**, ensuring accessibility, security, and optimal performance.
- **Deployment Steps**:
  - Prepare the project for production with necessary settings and configurations.
  - Use a requirements.txt file to specify dependencies.
  - Ensure static files and media are handled correctly in the deployed environment.

---

## Usage
### Endpoints Overview
#### Users:
- **Register**: `POST /api/account/register/`
- **Login**: `POST /api/account/login/`
- **Profile Management**: `GET/PUT/DELETE /api/account/profile/`

#### Posts:
- **Create Post**: `POST /api/account/posts/`
- **Retrieve Posts**: `GET /api/account/posts/`
- **Update/Delete Post**: `PUT/DELETE /api/account/posts/<int:pk>/`

#### Follow System:
- **Follow a User**: `POST /api/account/follow/`
- **Unfollow a User**: `DELETE /api/account/unfollow/<int:pk>/`

#### Feed:
- **View Feed**: `GET /api/account/feed/`

### Testing
- Use tools like **Postman** or **cURL** to interact with the API endpoints.
- Ensure proper authentication tokens are included in headers for secured endpoints.

---

## Future Enhancements
- **Likes and Comments**:
  - Add endpoints for users to like or comment on posts.
- **Notifications**:
  - Implement a notification system to inform users of interactions.
- **Media Uploads**:
  - Extend functionality for direct media file uploads.
- **Direct Messaging**:
  - Allow private messaging between users.

---

This API provides a robust foundation for a social media platform while offering opportunities for further enhancements and scalability.

