import * as vscode from "vscode";
import { getWebViewHtml } from "./page_template"


const SHOW_OPTIONS = {
    viewColumn: vscode.ViewColumn.Active,
    preserveFocus: false
};

export const WEBVIEW_OPTIONS = {
    enableCommandUris: true,
    enableFindWidget: true,
    enableScripts: true,
    retainContextWhenHidden: true,
};

export abstract class WebviewPage {
    protected static webview: vscode.WebviewPanel | undefined = undefined;
    private readonly viewType: string;
    protected abstract title: string;

    constructor(viewType: string) {
        this.viewType = viewType;
    }

    protected abstract renderContent(): string;

    protected createWebView(context: vscode.ExtensionContext) {
        const columnToShowIn = vscode.window.activeTextEditor
            ? vscode.window.activeTextEditor.viewColumn : undefined;
    
        if (WebviewPage.webview) {
            WebviewPage.webview.reveal(columnToShowIn);
        } else {
            WebviewPage.webview = vscode.window.createWebviewPanel(
                this.viewType, this.title, SHOW_OPTIONS, WEBVIEW_OPTIONS);
    
            WebviewPage.webview.webview.html
                    = getWebViewHtml(this.renderContent());
            WebviewPage.webview.onDidDispose(
                () => {WebviewPage.webview = undefined;},
                null,
                context.subscriptions
            );
        }
    }

    public display(context: vscode.ExtensionContext): void {
        this.createWebView(context);
    }
}