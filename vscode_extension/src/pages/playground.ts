import { WebviewPage } from "./page";

const TEMPLATE = `
<iframe width="96%" height="800px" src="https://prompt-fe.appspot.com?iframed=1" title="">
</iframe>`;


const VIEW_TYPE = 'prompt.playground';
export class PromptPlaygroundPage extends WebviewPage {
    protected title: string = 'Prompt Playground';

    public constructor() {
        super(VIEW_TYPE)
    }

    protected renderContent(): string {
        return TEMPLATE;
    }
}