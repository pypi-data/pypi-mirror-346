from judgeval.tracer import Tracer
import time
# loads from JUDGMENT_API_KEY env var
judgment = Tracer(project_name="ahh")

@judgment.observe(span_type="tool")
def my_tool():
    time.sleep(1)
    print("Hello world!")
    test_class = TestClass()
    test_class.test()

@judgment.observe(span_type="class")
class TestClass:
    @judgment.observe(span_type="tool")
    def test(self):
        print("hehehe")

my_tool()