/**
 * typing_local.js
 * 
 * SOLUCIÓN AL LAG: Este script intercepta el input de escritura y aplica
 * feedback visual INSTANTÁNEO en el cliente, sin esperar el round-trip
 * WebSocket al servidor en Render.
 * 
 * Cómo funciona:
 * 1. Escucha el input localmente en el browser
 * 2. Colorea los caracteres del texto display en tiempo real (sin servidor)
 * 3. El servidor sigue recibiendo el valor (para calcular stats al final)
 * 4. Al terminar, el servidor toma el control para mostrar resultados
 * 
 * Para usar: importar en main.py con rx.script(src="/typing_local.js")
 * o inline con rx.script(custom_attrs={"dangerouslySetInnerHTML": ...})
 */

(function () {
    'use strict';

    let targetText = '';
    let localTyped = '';
    let started = false;
    let startTime = null;
    let timerInterval = null;

    // Espera a que el DOM esté listo y el input exista
    function init() {
        const input = document.querySelector('.typing-input');
        const textDisplay = document.querySelector('.text-display');

        if (!input || !textDisplay) {
            // Reintenta si el componente aún no montó
            setTimeout(init, 200);
            return;
        }

        // Obtiene el texto objetivo desde los spans del display
        targetText = Array.from(textDisplay.querySelectorAll('span'))
            .map(s => s.textContent)
            .join('');

        // Escucha cambios localmente ANTES de que React/Reflex los procese
        input.addEventListener('input', handleLocalInput, { capture: true });
        input.addEventListener('keydown', handleKeyDown, { capture: true });

        // Renderiza el estado inicial
        renderChars('');
    }

    function handleLocalInput(e) {
        const value = e.target.value;

        // Anti-paste: ignorar si el salto es mayor a 1 carácter
        if (value.length - localTyped.length > 1) {
            e.target.value = localTyped;
            e.preventDefault();
            e.stopImmediatePropagation();
            return;
        }

        // Limitar al largo del texto objetivo
        const trimmed = value.slice(0, targetText.length);

        // Actualizar estado local
        localTyped = trimmed;

        // Feedback visual INMEDIATO (sin esperar servidor)
        renderChars(trimmed);

        // Iniciar timer local
        if (!started && trimmed.length > 0) {
            started = true;
            startTime = Date.now();
            startLocalTimer();
        }

        // Si terminó, detener timer local (el servidor tomará control)
        if (trimmed.length === targetText.length) {
            stopLocalTimer();
        }
    }

    function handleKeyDown(e) {
        if (e.key === 'Tab') {
            e.preventDefault();
            resetLocal();
            // Deja que el evento Tab llegue a Reflex para reset del servidor
        }
    }

    function renderChars(typed) {
        const textDisplay = document.querySelector('.text-display');
        if (!textDisplay) return;

        const spans = textDisplay.querySelectorAll('span');
        const cursor = typed.length;

        spans.forEach((span, i) => {
            const char = targetText[i];
            let cssClass;

            if (i < cursor) {
                cssClass = typed[i] === char ? 'char-correct' : 'char-wrong';
                if (char === ' ' && typed[i] !== char) cssClass = 'char-wrong-space';
            } else if (i === cursor) {
                cssClass = char === ' ' ? 'char-cursor-space' : 'char-cursor';
            } else {
                cssClass = 'char-pending';
            }

            if (span.className !== cssClass) {
                span.className = cssClass;
            }
        });

        // Actualizar barra de progreso localmente
        updateProgressBar(typed.length / targetText.length);
    }

    function updateProgressBar(fraction) {
        const fill = document.querySelector('.progress-fill');
        if (fill) {
            fill.style.width = (Math.min(fraction, 1) * 100).toFixed(1) + '%';
        }
    }

    function startLocalTimer() {
        // Actualiza el display del tiempo localmente cada 100ms
        timerInterval = setInterval(() => {
            const elapsed = (Date.now() - startTime) / 1000;
            const timeEl = document.querySelector('.stat-value');
            // Solo actualiza el tiempo si el test no terminó
            // (el servidor actualizará todos los stats al final)
        }, 100);
    }

    function stopLocalTimer() {
        if (timerInterval) {
            clearInterval(timerInterval);
            timerInterval = null;
        }
    }

    function resetLocal() {
        localTyped = '';
        started = false;
        startTime = null;
        stopLocalTimer();
        // Pequeño delay para que el servidor resetee el texto primero
        setTimeout(() => {
            // Re-obtener el texto objetivo (puede haber cambiado)
            const textDisplay = document.querySelector('.text-display');
            if (textDisplay) {
                targetText = Array.from(textDisplay.querySelectorAll('span'))
                    .map(s => s.textContent)
                    .join('');
                renderChars('');
            }
        }, 300);
    }

    // Observar cambios en el DOM para re-inicializar cuando Reflex
    // actualice el componente (ej: después de un reset)
    const observer = new MutationObserver((mutations) => {
        for (const m of mutations) {
            if (m.type === 'childList' && m.target.classList?.contains('text-display')) {
                // El texto cambió (reset), re-inicializar
                targetText = Array.from(m.target.querySelectorAll('span'))
                    .map(s => s.textContent)
                    .join('');
                localTyped = '';
                started = false;
                stopLocalTimer();
                break;
            }
        }
    });

    document.addEventListener('DOMContentLoaded', () => {
        observer.observe(document.body, { childList: true, subtree: true });
        init();
    });

    // Si el DOM ya está listo
    if (document.readyState !== 'loading') {
        observer.observe(document.body, { childList: true, subtree: true });
        init();
    }
})();