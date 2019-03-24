import os,sys,glob
from Preprocess import PreprocessClass

p = PreprocessClass()

project_path = r'/Users/eshwar/Documents/projects/sentiment_analysis_on_movie_reviews/'
dataset_path = project_path+"data/dataset/aclImdb/"
train_pos_path = dataset_path+"train/pos/"
train_neg_path = dataset_path+"train/neg/"
test_pos_path = dataset_path+"test/pos/"
test_neg_path = dataset_path+"test/neg/"
target_path = project_path+"data/dataset_preprocessed/"
target_train_file_name = "full_train_preprocessed.txt"
target_test_file_name = "full_test_preprocessed.txt"
file_names = list(range(12500))
file_names = [str(file_name)+"_" for file_name in file_names]

def get_file_names(path):
    os.chdir(path)
    ordered_file_names = []
    for each_file_name in file_names:
        temp_file_name = glob.glob(each_file_name+"*")
        ordered_file_names.append(" ".join(temp_file_name))
    return ordered_file_names

def preprocess_files(path, file_names, target_name):
    target_file_name = target_path+target_name
    mode = ''
    if os.path.exists(target_file_name):
        mode = 'a'
    else:
        mode = 'w'
    with open(target_file_name, mode) as outfile:
        for filename in file_names:
            with open(path+filename) as infile:
                for line in infile:
                    preprocessed_line = p.pre_process(line)
                    outfile.write(preprocessed_line)
                outfile.write("\n")


if __name__ == '__main__':
    #train pos
    ordered_train_pos = get_file_names(train_pos_path)
    preprocess_files(train_pos_path, ordered_train_pos, target_train_file_name)
    print("train pos completed")
    #train neg
    ordered_train_neg = get_file_names(train_neg_path)
    preprocess_files(train_neg_path, ordered_train_neg, target_train_file_name)
    print("train neg completed")
    #test pos
    ordered_test_pos = get_file_names(test_pos_path)
    preprocess_files(test_pos_path, ordered_test_pos, target_test_file_name)
    print("test pos completed")
    #test neg
    ordered_test_neg = get_file_names(test_neg_path)
    preprocess_files(test_neg_path, ordered_test_neg, target_test_file_name)
    print("test neg completed")
    print("dataset preprocessed !!")