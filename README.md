 # Recipe Finder Web Application
## 1. Introduction

### Purpose and Objectives
The point of this app is to help people find recipes that use the ingredients they already have. It is supposed to make cooking easier and cut down on food waste by suggesting meals that don't need a lot of extra ingredients.

### Project Overview
Flask was used to make this project a web app. It uses the Spoonacular API to get information about recipes. People who use the web type in the ingredients they have and, if they want to, apply filters. The system then automatically returns the recipe results, including all the ingredients they need and instructions on how to make the meal they want.

---

## 2. Problem Definition and Requirements

### Problem Description
People often don’t know what to cook with the ingredients they have at home. This can lead to wasted food or unnecessary shopping. This application helps solve that problem by suggesting recipes based on available ingredients.

### Functional Requirements
- User can enter ingredients they have
- System searches for recipes using those ingredients
- User can filter results by diet (vegan, vegetarian, gluten-free)
- User can filter by meal type (breakfast, dinner)
- System shows recipe details like ingredients and instructions

### Non-Functional Requirements
- The app should respond quickly
- It should be easy to use
- It should handle API errors properly
- Code should be easy to understand and maintain

---

## 3. Design and Implementation

### Object-Oriented Design
The program uses object-oriented programming (OOP):

- **Encapsulation**: Classes like `Recipe`, `Ingredient`, and `RecipeFinder` store data and related functions together.
- **Abstraction**: The `Ingredient` class acts as a base class and defines methods that other classes must implement.
- **Inheritance**: `OwnedIngredient` and `MissingIngredient` are based on the `Ingredient` class.
- **Polymorphism**: These subclasses behave differently depending on whether the ingredient is missing or not.

### Design Patterns
- **Singleton Pattern**: Only one `RecipeFinder` object is created to handle API requests.
- **Facade Pattern**: The method `search_by_ingredients()` hides complex API calls and makes it easy to use.

### Class Structure
- `Ingredient` – base class for ingredients  
- `OwnedIngredient` – ingredient the user has  
- `MissingIngredient` – ingredient the user does not have  
- `Recipe` – stores recipe information  
- `RecipeFinder` – handles API requests and logic  

### Algorithms and Data Structures
- Lists are used to store ingredients and recipes  
- Dictionaries are used to match recipe IDs with details  
- Filtering is used to apply diet and meal type options  
- Strings are used to format input and instructions  

---

## 4. Development Process

### Tools and Environment
- Python programming language  
- Flask - a micro web framework 
- Spoonacular API  
- Requests library (allows to send HTTP requests using Python)
- VS Code  

### Development Steps
1. Planned what the app should do  
2. Designed the classes and structure  
3. Connected to the API  
4. Built the web interface using Flask  
5. Added filtering features
6. Added saving to cart and favourites features  
7. Tested and fixed issues  

---

## 5. Results and Demonstration

### Application Features
- Search recipes by ingredients  
- Filter by diet and meal type  
- Show which ingredients are missing  
- Display cooking instructions  
- Get real-time data from API  

### Demonstration
Example:
1. User enters ingredients (e.g., "egg, milk")  
2. Selects filters  
3. Gets a list of recipes  

*Search page*
![Search Page](searchpage.png)
*Results page*
![Results Page](resultspage.png)

---

## 6. Testing and Validation

### Testing Procedures
- Tested with different ingredient inputs  
- Checked how API responses are handled  
- Tested edge cases like empty input  

### Results and Issues
- App works correctly for most inputs  
- Handles missing data from API  
- Some API responses were inconsistent but were handled in the code  

---

## 7. Conclusion and Future Work

### Summary of Achievements
- Built a working web application using Flask  
- Connected to an external API  
- Used object-oriented programming concepts  
- Created a clear and structured program  

### Future Improvements
- Add user accounts  
- Improve the design of the interface  
- Add caching to improve performance  
- Add more filters  

---

## 8. Build/Run instructions

### Requirements

- Python 3 installed
- Internet connection for Spoonacular API requests

### Installation

```
pip install flask requests
```
### Running the Application
1. Open the project folder in VS Code or terminal
2. Run the application:
```
python app.py
```
3. Open your browser and go to:
```
http://127.0.0.1:5000
```
## 9. Contributions

### Contribution details
Daniel took up the programming task and Augustas made both readme.md file and presentation slides. Both group members worked as a group and consultated with each other if any problems occured. 
## References
- https://spoonacular.com/food-api  
- https://flask.palletsprojects.com/  
- https://docs.python-requests.org/  
