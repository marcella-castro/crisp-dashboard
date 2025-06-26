document.addEventListener('DOMContentLoaded', function() {
    document.body.addEventListener('click', function(e) {
        // Verifica se clicou no email ou no ícone
        if (e.target && (e.target.id.startsWith("email-span-") || e.target.id.startsWith("clipboard-icon-") || e.target.id.startsWith("clipboard-span-"))) {
            // Descobre o email
            let email = "";
            if (e.target.id.startsWith("email-span-")) {
                email = e.target.textContent.trim();
            } else if (e.target.id.startsWith("clipboard-icon-")) {
                // O irmão anterior é o span do email
                email = e.target.parentElement.previousSibling.textContent.trim();
            } else if (e.target.id.startsWith("clipboard-span-")) {
                // O irmão anterior é o span do email
                email = e.target.previousSibling.textContent.trim();
            }
            if (email) {
                navigator.clipboard.writeText(email);
                // Troca o ícone
                let iconId = "clipboard-icon-" + email;
                let icon = document.getElementById(iconId);
                if (icon) {
                    icon.className = "bi bi-clipboard-check-fill";
                    icon.style.color = "#198754";
                    setTimeout(function() {
                        icon.className = "bi bi-clipboard";
                        icon.style.color = "#888";
                    }, 1200);
                }
            }
        }
    });
});