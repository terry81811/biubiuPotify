import os
import nltk

# file2 = "input/test_review_content"
file2 = "../subset_review_content"

# os.system("python ../add_review_id.py ../../../data/data/YelpNYC/metadata input/test_metadata")
# os.system("python ../add_review_id_content.py ../../../data/data/YelpNYC/reviewContent input/test_review_metadata")

os.system("python WordCount_reviews.py " + file2 + " output/output_wordcount.txt")
os.system("python biGram.py " + file2 + " output/output_biGram.txt")
os.system("python allCapitalCount.py " + file2 + " output/output_AllCapital.csv")
os.system("python countCapital.py " + file2 + " output/output_PC.csv")
os.system("python ratioPPwordCount.py " + file2 + " output/output_PP1.csv")
os.system("python excSentenceCount.py " + file2 + " output/output_RES.csv")
os.system("python sentimentAnalysis.py " + file2 + " output/output_SW+OW.csv")
os.system("python uniGram.py " + file2 + " output/output_uniGram.txt")
os.system("python codeTable.py output/output_uniGram.txt output/output_DL_u.csv output/dict_uniGram.csv")
os.system("python codeTable.py output/output_biGram.txt output/output_DL_b.csv output/dict_biGram.csv")