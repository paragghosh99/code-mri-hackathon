from google.cloud import firestore

db = firestore.Client()


def save_file_analysis(repo: str, file_data: dict):

    collection = db.collection("repo_analysis")

    doc_ref = collection.document(repo)

    doc_ref.set(
        {
            "files": firestore.ArrayUnion([file_data])
        },
        merge=True
    )