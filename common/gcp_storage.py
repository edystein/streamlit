
# @st.experimental_memo(ttl=600)
def read_file(client, bucket_name, file_path, b_decode_as_string=False):
    """
    read binary or txt file from gcp
    :param client:
    :param bucket_name:
    :param file_path:
    :param b_decode_as_string:
    :return:
    """
    bucket = client.bucket(bucket_name)
    if b_decode_as_string:
        content = bucket.blob(file_path).download_as_string().decode("utf-8")
    else:
        content = bucket.blob(file_path).download_as_bytes()
    return content
