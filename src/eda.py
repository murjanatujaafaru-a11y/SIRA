
import pprint

class DataExplorer:

    def basic_summarry(self, df):
        print(df.info())
        print(df.describe(include="all"))

    def show_missing_values(self, df):
        print("missing values:") 
        # Optional: You might want to change this to df.isnull().sum() later to actually see the missing counts!
        print(df.columns.tolist()) 
        
    def show_columns(self, df):
        print("Columns:")
        print(df.columns.tolist())

    def show_shape(self, df):
        print("Shape:")
        print(df.shape)

    def show_random_sample(self, df):
        print("Random Sample:")
        print(df.sample(n=5))
        
    def duplicate_rows(self, df):
        duplicate_count = df.duplicated().sum()
        pprint.pprint(f"Number of duplicate rows: {duplicate_count}")

    
    def print_header(self, title):
        """Generates a clean visual header for terminal sections."""
        border = "=" * 50
        print(f"\n{border}")
        print(f"{title.upper().center(50)}")
        print(f"{border}\n")