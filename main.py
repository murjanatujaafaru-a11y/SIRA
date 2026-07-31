from src.data_loader import DataLoader
from src.eda import DataExplorer
from src.utils import print_header
from src.preprocessing import DataCleaner


#print header

def main():
    loader = DataLoader()
    df = loader.load_data()
    print(df.head())

    explorer = DataExplorer()
    # explorer.basic_summary(df)
    df = loader.load_data()
    explorer.show_missing_values(df)
    explorer.show_columns(df)
    # explorer.show_shapes(df)
    explorer.show_random_sample(df)

def load_data(self):
    # ... your loading logic that creates a list of data ...
    
    # Make sure it returns this:
    return pd.DataFrame(raw_data_list)

   
def main():
    # 1. Initialize data components
    loader = DataLoader()
    df = loader.load_data()
    explorer = DataExplorer()
    
    # 2. Run EDA sections using the utility header
    print_header("Data Head Preview")
    print(df.head().to_string(index=False))

    print_header("Missing Values Analysis")
    explorer.show_missing_values(df)
    
    print_header("Dataset Columns")
    explorer.show_columns(df)
    
    print_header("Random Data Sample")
    explorer.show_random_sample(df)

    loader = DataLoader()
    cleaner = DataCleaner()

    df = loader.load_data()


    print("Before Cleaning")
    print(df.shape)

    df = cleaner.remove_missing(df)
    df = cleaner.remove_duplicates(df)
    df = cleaner.strip_spaces(df)
    df = cleaner.lowercase(df)

    print("After Cleaning")
    print(df.shape)







   



if __name__ == "__main__":
    main()
   
