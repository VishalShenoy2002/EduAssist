function startTypeWriter() {

    const typewriterElements = document.querySelectorAll('.type-writer');

    typewriterElements.forEach(element => {
        const text = element.textContent;
        element.textContent = "";
        let charIndex = 0;

        function typeWriter() {
            if (charIndex < text.length) {
                element.innerHTML += text.charAt(charIndex);
                charIndex++;
                const currentChar = text.charAt(charIndex - 1);

                // Adjust delays for punctuation
                const delay = (currentChar === ',' || currentChar === '.') ? 500 : 50;

                setTimeout(typeWriter, delay);
            }
        }

        // Initial start delay
        setTimeout(typeWriter, 2000);
    });
}
document.addEventListener("DOMContentLoaded",startTypeWriter);