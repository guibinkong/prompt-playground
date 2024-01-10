import {workspace, ExtensionContext, WorkspaceConfiguration} from 'vscode';

const CONFIG_NAME = 'pp'; 

class Config {
    private readonly config: WorkspaceConfiguration;

    constructor() {
        this.config = workspace.getConfiguration(CONFIG_NAME, undefined);
    }

    public getEnable(): boolean {
        return this.config.get('enable', true);
    }

    public getEnableState(context: ExtensionContext): boolean {
        let enabled : boolean | null =  context.globalState.get("enable", null);
        if (enabled === null) {
            enabled = config.getEnable();
        }
        return enabled;
    }

    public async setEnable(newVal: boolean) {
        await this.config.update("privacy", newVal, true);
    }


    public getPrivacy(): boolean | null {
        return this.config.get('privacy', null);
    }

    public async setPrivacy(newVal: boolean) {
        await this.config.update("privacy", newVal, true);
    }

    public getPrivacyState(context: ExtensionContext): boolean | null {
        let privacy : boolean | null =  context.globalState.get("privacy", null);
        if (privacy === null) {
            privacy = this.getPrivacy();
        }
        return privacy;
    }

    public getTemperature(): number {
        return this.config.get('temperature', 0.8);
    }

    public getTemperatureState(context: ExtensionContext): number {
        let state : number | null =  context.globalState.get("temperature", null);
        if (state === null) {
            state = this.getTemperature();
        }
        return state;
    }

    public async setTemperature(newVal: number) {
        await this.config.update("temperature", newVal, true);
    }

    public getTopP(): number {
        return this.config.get('topp', 0.95);
    }

    public getTopPState(context: ExtensionContext): number {
        let state : number | null =  context.globalState.get("topp", null);
        if (state === null) {
            state = this.getTopP();
        }
        return state;
    }

    public async setTopP(newVal: number) {
        await this.config.update("topp", newVal, true);
    }

    public getTopK(): number {
        return this.config.get('topk', 0.0);
    }

    public getTopKState(context: ExtensionContext): number {
        let state : number | null =  context.globalState.get("topk", null);
        if (state === null) {
            state = this.getTopK();
        }
        return state;
    }

    public async setTopK(newVal: number) {
        await this.config.update("topk", newVal, true);
    }
}

const config = new Config();
export default config;