document.addEventListener('DOMContentLoaded', () => { document.querySelectorAll('.tab').forEach(tab => { tab.addEventListener('click', () => { document.querySelectorAll('.tab').forEach(t => t.classList.remove('active')); document.querySelectorAll('.content-section').forEach(sec => sec.classList.remove('active')); tab.classList.add('active'); document.getElementById(tab.dataset.tab).classList.add('active'); }); });

document.querySelectorAll('.sub-tab').forEach(subTab => { subTab.addEventListener('click', () => { document.querySelectorAll('.sub-tab').forEach(st => st.classList.remove('active')); document.querySelectorAll('.sub-tab-content').forEach(stc => stc.classList.remove('active')); subTab.classList.add('active'); document.getElementById(subTab.dataset.subtab).classList.add('active'); }); }); });


