let nav = document.getElementById("nav");
let active = 0;
let content_paths = [
  "content/me.txt",
  "content/family.txt",
  "content/friends.txt",
  "content/goals.txt",
  "content/hobbies.txt",
  "content/school.txt",
];

change_content(0);

function change_content(clicked) {
  active = clicked;
  update_nav();
  update_content();
}

// Update Nav
function update_nav() {
  var children = nav.children;
  for (var i = 0; i < children.length; i++) {
    var child = children[i].children[0];
    child.classList.remove("active");
    if (active == i) {
      child.classList.add("active");
    }
  }
}

// Grab Content
function update_content() {
  var content = new XMLHttpRequest();
  content.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("error").style.display = "none";
      document.getElementById("content").innerHTML = this.responseText;
    }
    else if (this.status == 404) {
      document.getElementById("error").style.display = "block";
      document.getElementById("content").innerHTML = "";
    }
  };
  content.open("GET", content_paths[active], true);
  content.send();
}
