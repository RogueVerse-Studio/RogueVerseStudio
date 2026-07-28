const toggle=document.querySelector('.nav-toggle');const links=document.querySelector('.nav-links');toggle?.addEventListener('click',()=>links.classList.toggle('open'));
document.querySelectorAll('[data-year]').forEach(el=>el.textContent=new Date().getFullYear());
