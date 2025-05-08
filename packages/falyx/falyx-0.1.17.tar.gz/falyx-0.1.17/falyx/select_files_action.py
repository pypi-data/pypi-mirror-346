
class SelectFilesAction(BaseAction):
    def __init__(
        self,
        name: str,
        directory: Path | str = ".",
        title: str = "Select a file",
        prompt_message: str = "Choose > ",
        style: str = OneColors.WHITE,
        suffix_filter: str | None = None,
        return_path: bool = True,
        console: Console | None = None,
        session: PromptSession | None = None,
    ):
        super().__init__(name)
        self.directory = Path(directory).resolve()
        self.title = title
        self.prompt_message = prompt_message
        self.suffix_filter = suffix_filter
        self.style = style
        self.return_path = return_path
        self.console = console or Console()
        self.session = session or PromptSession()

    async def _run(self, *args, **kwargs) -> Any:
        context = ExecutionContext(name=self.name, args=args, kwargs=kwargs, action=self)
        context.start_timer()
        try:
            await self.hooks.trigger(HookType.BEFORE, context)

            files = [
                f
                for f in self.directory.iterdir()
                if f.is_file()
                and (self.suffix_filter is None or f.suffix == self.suffix_filter)
            ]
            if not files:
                raise FileNotFoundError("No files found in directory.")

            options = {
                str(i): SelectionOption(
                    f.name, f if self.return_path else f.read_text(), self.style
                )
                for i, f in enumerate(files)
            }
            table = render_selection_dict_table(self.title, options)

            key = await prompt_for_selection(
                options.keys(),
                table,
                console=self.console,
                session=self.session,
                prompt_message=self.prompt_message,
            )

            result = options[key].value
            context.result = result
            await self.hooks.trigger(HookType.ON_SUCCESS, context)
            return result
        except Exception as error:
            context.exception = error
            await self.hooks.trigger(HookType.ON_ERROR, context)
            raise
        finally:
            context.stop_timer()
            await self.hooks.trigger(HookType.AFTER, context)
            await self.hooks.trigger(HookType.ON_TEARDOWN, context)
            er.record(context)
