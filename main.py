import json
import streamlit as st

class BookCollection:
    """A class to manage a collection of books , allowing users  to store and organize books and their reading materials"""

    def __init__(self):
        """Initialize the book collection with an empty list of books and set up file storage"""
        self.book_list = []
        self.storage_file = "books_data.json"
        self.read_from_file()

    def read_from_file(self):
        """Load saved books from a JSON file into memory.
        If the file does'nt exist or is corrupted, start with an empty collection"""
        try:
            with open(self.storage_file, "r") as file:
                self.book_list = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.book_list = []

    def save_to_file(self):
        """Save the current list of books to the JSON file for permanent storage"""
        with open(self.storage_file, "w") as file:
            json.dump(self.book_list,file,indent=4)

    def create_new_book(self,title,author,year,genre,read):
        """Prompt user for details and add a new book to the collection"""

        new_book = {
            "title":title,
            "author":author,
            "year":year,
            "genre":genre,
            "read":read
        }

        self.book_list.append(new_book)
        self.save_to_file()
       

    def delete_book(self, book_title, book_author):
        """Remove a book from the collection via its title or author"""
        books_to_remove = [
            book for book in self.book_list 
            if (book_title and book["title"].lower() == book_title.lower()) or 
               (book_author and book["author"].lower() == book_author.lower())
        ]

        if books_to_remove:
            for book in books_to_remove:
                self.book_list.remove(book)
            self.save_to_file()
        else:
            pass  # No books found, but no Streamlit messages inside the function


    def find_book(self,search_text):
        """Search for a book by title or the author's name"""
        return [book for book in self.book_list if search_text.lower() in book["title"].lower() or search_text.lower() == book["author"].lower()
                ]


    def update_book(self,old_title,new_title,new_author,new_year,new_genre,new_read):
        """Update the information of a book"""
      
        for book in self.book_list:
            if book["title"].lower() == old_title.lower():
             
                book["title"] = new_title or book["title"]
                book["author"] = new_author or book["author"]
                book["year"] = new_year or book["year"]
                book["genre"] = new_genre or book["genre"]
                book["read"] = new_read
                self.save_to_file()
                return True
            return False
       


    def display_all_books(self):
        """Display all books in the collection with their details"""
        if not self.book_list:
            print("No books in your collection yet.\n")
            return
        else:
            print("\nAll books in your collection:")
            for index, book in enumerate(self.book_list,1):
                reading_status = "Read" if book["read"] else "Not Read"
                print(
                    f"{index}.{book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {reading_status}"
                )
            print()

    def show_reading_progress(self):
        """Calculate and display statistics about your reading progress"""
        total_books = len(self.book_list)
        completed_books = sum(1 for book in self.book_list if book["read"])
        return total_books,completed_books
    
book_manager = BookCollection()

st.title("📚Welcome to your personal Library Manager📚")

menu = {
    "📖Add Book" : "add book",
    "❌Remove book": "remove book",
    "🔎Search Book":"search book",
    "🖋️Update Book":"update book",
    "📚View Your Collection":"View all books",
    "✅Reading Progress":"reading progress",
    "🚪Exit":"exit"

}

choice = st.sidebar.selectbox("Menu",list(menu.keys()))

if choice == "📖Add Book":
    st.subheader("Add a new book")
    title = st.text_input("Book Title")
    author = st.text_input("Author Name")
    year = st.text_input("Publication Year")
    genre = st.text_input("Book Genre")
    read = st.checkbox("Have you read this book?")
    if st.button("Add Book"):
        book_manager.create_new_book(title,author,year,genre,read)
        st.success("🏆Book added Successfully!✅")
elif choice == "❌Remove book":
    st.subheader("Remove a book")
    book_title = st.text_input("Enter the title of the book to remove (optional)")
    book_author = st.text_input("Enter the author of the book to remove (optional)")

    if st.button("🗑️ Remove Book"):
        if not book_title and not book_author:
            st.warning("Please enter at least a title or an author to remove a book.")
        else:
            before_count = len(book_manager.book_list)
            book_manager.delete_book(book_title, book_author)
            after_count = len(book_manager.book_list)

            if before_count == after_count:
                st.warning("No matching books found!")
            else:
                st.success("Book removed successfully!")


elif choice == "🔎Search Book":
    st.subheader("🔎 Search for Books")
    search_text = st.text_input("Search for books by Title or Author")

    if st.button("Search"):
        results = book_manager.find_book(search_text)

        if results:
            for book in  results:
                
                col1,col2 = st.columns([3,1])

                with col1:
                    st.write(f"📗** {book['title']} by {book['author']} - {book["year"]} - {book['genre']}")

elif choice == "🖋️Update Book":
    st.subheader("Update Book Details")
    old_title = st.text_input("Enter the title of the book you would like to update")
    new_title = st.text_input("Enter title (leave blank to keep the same)")
    new_author = st.text_input("Enter Author (leave blank to keep the same)")
    new_year = st.text_input("Enter Published Year (leave blank to keep the same)")
    new_genre = st.text_input("Enter Genre (leave blank to keep the same)")
    new_read = st.checkbox("Have you read this book?")
    if st.button("Update Book Details"):
        if book_manager.update_book(old_title,new_title,new_author,new_year,new_genre,new_read):
            st.success("Book updated successfully!")
        else:
            st.warning("😔 Book not found")

elif choice == "📚View Your Collection":
    st.subheader("📚 This is your Collection")
    books = book_manager.book_list
    if books :
        for book in books:
            status = "☑️Read"if book['read'] else "⛔ Not Read"
            st.write(f"📗** {book['title']} by {book['author']} - ({book["year"]}) - {book['genre']} | Status ={status}")

    else:
        st.info("No Books in your collection yet")

elif choice ==  "✅Reading Progress":
    st.subheader("Your reading progress")
    total , completed = book_manager.show_reading_progress()
    st.write("📚Total Books :" , total)
    st.write("✅Books Read :", completed)
    progress = ((completed/total)* 100) if total > 0 else 0
    st.progress(progress/100)
    st.write(f"Progress: {progress:.2f}%")

elif choice == "🚪Exit":
    st.balloons()
    st.success("🎉Thank you for using personal libarray manager. See you nest time!😊")
    
 
    


                
            
