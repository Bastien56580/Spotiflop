const button = document.getElementById('submit')

                const titre = document.querySelector('input[name="titre"]')
                const artiste = document.querySelector('input[name="artiste"]')
                const musique = document.querySelector('input[name="musique"]')

                let file = null;

                musique.addEventListener('change', (event) => {
                    file = event.target.files[0];
                });

                button.addEventListener('click', async (event) => {
                    event.preventDefault()
                    event.stopPropagation()
                    if (isFilled()) {
                        let formData = new FormData()
                        formData.append('titre', titre.value);
                        formData.append('artiste', artiste.value);
                        formData.append('musique', file);

                        const response = await fetch("/musique/ajouterTitre", {
                            method: "POST",
                            body: formData
                        });
                        if (response.ok) {
                            window.location.href = "/musique/titres";
                        }

                    }
                })

                function isFilled() {
                    return titre.value !== '' && artiste.value !== '' && file !== null
                }
