from flask import Flask, render_template, request
import requests

app = Flask(__name__)

url_base = "https://coomer.su/api/v1/posts"
cookie = "eyJfcGVybWFuZW50Ijp0cnVlLCJhY2NvdW50X2lkIjo3MjEwODR9.Zfjphw.zkkHYEE7EfT_IRjFqzZOo3F_jo0"
headers = {
    "accept": "application/json",
    "Cookie": cookie
}
posts_per_page = 50



def get_posts(offset):
    response = requests.get(url_base, headers=headers, params={"o": offset})
    base_url = "https://coomer.su"
    if response.status_code == 200:
        data = response.json()
        posts = []
        for post in data:
            attachments = post.get("attachments", [])  # Obtener la lista de attachments o una lista vacía si no hay attachments
            image_urls = [base_url + attachment["path"] for attachment in attachments] if attachments else []  # Construir la lista de URLs de imágenes
            posts.append({
                "id": post["id"],
                "user": post["user"],
                "service": post["service"],
                "title": post["title"],
                "content": post["substring"],
                "published": post["published"],
                "image_urls": image_urls  # Agregar la lista de URLs de imágenes al diccionario del post
            })
        return posts
    else:
        return None
        
#def get_posts(offset):
#    response = requests.get(url_base, headers=headers, params={"o": offset})
#    if response.status_code == 200:
#        data = response.json()
#        posts = [{"title": post["title"], "id": post["id"], "user": post["user"], "service": post["service"],  "content": post["substring"], "published": post["published"], "file": post["file"], "attachments": post["attachments"]} for post in data]
#        return posts
#    else:
#        return None
        
#def get_posts(offset):
#    response = requests.get(url_base, headers=headers, params={"o": offset})
#    if response.status_code == 200:
#        return response.json()
#    else:
#        return None


@app.route('/')
def index():
    page = request.args.get('page', default=1, type=int)
    offset = (page - 1) * posts_per_page
    posts = get_posts(offset)
    return render_template('index.html', posts=posts, page=page)


if __name__ == '__main__':
    app.run(debug=True)
    