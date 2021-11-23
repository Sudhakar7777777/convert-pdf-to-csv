# Import Module
import tabula

# define pdf record columns
cols = ['Country', 'Label', 'Sold', 'System',
        'Description', 'Rating', 'Store']
max_cols = 7
newline_char = '\r'

# define pdf page range
first_page = 4
last_page = 17
pages = [*range(first_page, last_page + 1, 1)]


def remove_excess_columns(df, max_cols=max_cols):
    curr_columns = df.shape[1]
    remove_cols = [*range(max_cols, curr_columns, 1)]
    df.drop(df.columns[remove_cols], axis=1, inplace=True)


def process_pdf_file():
    pages_df = None
    for page in pages:
        print(f"processing page {page}...")
        # read specific page from pdf file
        page_df = tabula.read_pdf('ratings.pdf', pages=page)[0]
        # remove excess columns
        if(page_df.shape[1] > max_cols):
            print(f"Page shape: {page_df.shape}")
            remove_excess_columns(page_df)
            print(f"Adjusted Page shape: {page_df.shape}")
        # print(f"Page shape: {page_df.columns}")
        # set custom columns
        page_df.columns = cols
        # remove unwanted rows / records
        page_df.drop(page_df[page_df['System'] ==
                     "SYSTEM"].index, inplace=True)
        page_df.drop(page_df[page_df['System'].isnull()].index, inplace=True)
        # save page
        if pages_df is None:
            pages_df = page_df
        else:
            pages_df = pages_df.append([page_df])
    # backfill Country column
    pages_df['Country'].fillna(method='ffill', inplace=True)
    # fill nan with false
    pages_df['Sold'].fillna(0, inplace=True)
    pages_df.loc[pages_df['Sold'] == "✓", 'Sold'] = 1
    pages_df.replace(newline_char, ' ', regex=True, inplace=True)
    # remove unwanted column
    # pages_df.drop('none', axis=1, inplace=True)
    # save to file
    print(f"Saving file of shape: {pages_df.shape}")
    pages_df.to_csv('ratings.csv', index=False)
    print(f"Here is preview of file:\n{pages_df.head(5)}")


def main():
    process_pdf_file()


if __name__ == "__main__":
    main()
