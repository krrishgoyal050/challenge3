import { render, screen } from "@testing-library/react";
import Home from "@/app/page";

jest.mock("recharts", () => ({
  ResponsiveContainer: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
  AreaChart: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
  Area: () => <div />,
  BarChart: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
  Bar: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
  Cell: () => <div />,
  CartesianGrid: () => <div />,
  Tooltip: () => <div />,
  XAxis: () => <div />,
  YAxis: () => <div />
}));

describe("Home", () => {
  it("renders dashboard, calculator, and assistant", () => {
    render(<Home />);
    expect(screen.getByText("Carbon Footprint Awareness Platform")).toBeInTheDocument();
    expect(screen.getByText("Carbon Calculator")).toBeInTheDocument();
    expect(screen.getByText("AI Sustainability Assistant")).toBeInTheDocument();
  });
});
