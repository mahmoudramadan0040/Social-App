let addFriends = document.querySelectorAll('.addFriend');
let pending = document.createElement('div');
pending.textContent = 'pending';
addFriends.forEach((item) => {
  item.addEventListener('click', (e) => {
    e.target.parentElement.append(pending);
    e.target.remove();
  });
});
