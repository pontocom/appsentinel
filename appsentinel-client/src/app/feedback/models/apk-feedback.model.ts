import { Vulnerability } from "./vulnerability.model";

export class ApkFeedback {
    public OWASPCategory: string;
    public detailedFeedback: Vulnerability[];
}