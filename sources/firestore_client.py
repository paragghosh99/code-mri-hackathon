from google.cloud import firestore

db = firestore.Client()


# def save_file_analysis(repo: str, file_data: dict):

#     collection = db.collection("repo_analysis")

#     doc_ref = collection.document(repo)

#     doc_ref.set(
#         {
#             "files": firestore.ArrayUnion([file_data])
#         },
#         merge=True
#     )

# def save_file_analysis(repo: str, file_data: dict):

#     db.collection("repo_analysis") \
#       .document(repo) \
#       .collection("files") \
#       .document(file_data["file"]) \
#       .set(file_data)

def save_file_analysis(repo: str, file_data: dict):

    # replace "/" so Firestore doc id is valid
    doc_id = file_data["file"].replace("/", "__")

    db.collection("repo_analysis") \
      .document(repo) \
      .collection("files") \
      .document(doc_id) \
      .set(file_data)