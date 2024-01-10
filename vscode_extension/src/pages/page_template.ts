
export function getWebViewHtml(content?: string) {
    return `<!DOCTYPE html>
<html lang="en" style="margin: 0; padding: 0; min-width: 100%; min-height: 100%">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Prompt Playground</title>
    </head>
    <body style="margin: 0; padding: 0; width: 100%; height: 100%">
        <div>
            <div>${content}</div>
        </div>
    </body>
</html>`;
}
