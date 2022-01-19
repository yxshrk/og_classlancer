document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.likelink').forEach(link => {
        link.onclick = function() {
            const postid = this.dataset.postid;
            const curr = document.querySelector(`#span${postid}`);
            fetch(`/togglelike/${postid}`);

            if (this.innerHTML === '🤍') {
                this.innerHTML = '❤️';
                curr.innerHTML = parseInt(curr.innerHTML) + 1;
            } else {
                this.innerHTML = '🤍';
                curr.innerHTML = parseInt(curr.innerHTML) - 1;
            }
        };
    });

});