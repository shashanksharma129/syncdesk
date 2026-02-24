// ABOUTME: Temporary page to demonstrate all UI primitives.
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Select } from "@/components/ui/Select";
import { Textarea } from "@/components/ui/Textarea";
import { Badge } from "@/components/ui/Badge";
import { Alert } from "@/components/ui/Alert";

export default function UiPreviewPage() {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "1.5rem", paddingBottom: "2rem" }}>
      <h1>UI Preview</h1>
      <section>
        <h2>Buttons</h2>
        <div style={{ display: "flex", flexWrap: "wrap", gap: "0.5rem" }}>
          <Button variant="primary">Primary</Button>
          <Button variant="secondary">Secondary</Button>
          <Button variant="ghost">Ghost</Button>
          <Button variant="danger">Danger</Button>
          <Button variant="primary" disabled>Disabled</Button>
        </div>
      </section>
      <section>
        <h2>Input</h2>
        <Input id="demo-input" label="Phone number" placeholder="+1 555 000 0000" />
        <Input id="demo-input-err" label="With error" error="Please enter a valid number." />
      </section>
      <section>
        <h2>Select</h2>
        <Select id="demo-select" label="Category" placeholder="Choose one" options={[{ value: "a", label: "Academic" }, { value: "t", label: "Transport" }]} />
      </section>
      <section>
        <h2>Textarea</h2>
        <Textarea id="demo-ta" label="Description" placeholder="Enter details..." rows={3} />
      </section>
      <section>
        <h2>Badges</h2>
        <div style={{ display: "flex", flexWrap: "wrap", gap: "0.5rem" }}>
          <Badge variant="pending">Pending</Badge>
          <Badge variant="in_progress">In Progress</Badge>
          <Badge variant="resolved">Resolved</Badge>
          <Badge variant="urgent">Urgent</Badge>
          <Badge variant="neutral">Neutral</Badge>
        </div>
      </section>
      <section>
        <h2>Alerts</h2>
        <Alert variant="info" title="Info">Office hours: Mon–Fri 8am–4pm.</Alert>
        <Alert variant="success">Your request was submitted.</Alert>
        <Alert variant="warning" title="Notice">Please wait 30 minutes before creating another ticket.</Alert>
        <Alert variant="error" title="Error">Something went wrong. Please try again.</Alert>
      </section>
    </div>
  );
}
